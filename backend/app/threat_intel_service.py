import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models

class ThreatIntelligenceService:
    def __init__(self):
        self.cisa_kev_url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
        self.update_interval = timedelta(hours=6)
        self.last_update = None

    async def fetch_cisa_kev(self) -> Optional[Dict]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.cisa_kev_url, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"CISA KEV: Fetched {len(data.get('vulnerabilities', []))} known exploited vulnerabilities")
                        return data
                    else:
                        print(f"CISA KEV fetch failed with status {response.status}")
                        return None
        except asyncio.TimeoutError:
            print("CISA KEV fetch timed out")
            return None
        except Exception as e:
            print(f"ERROR fetching CISA KEV: {e}")
            return None

    async def ingest_cisa_kev(self, db: Session) -> int:
        data = await self.fetch_cisa_kev()
        if not data:
            return 0

        vulnerabilities = data.get("vulnerabilities", [])
        ingested_count = 0

        for vuln in vulnerabilities:
            try:
                existing = db.query(models.ThreatIntel).filter(
                    models.ThreatIntel.title == vuln.get("cveID")
                ).first()

                if not existing:
                    threat_intel = models.ThreatIntel(
                        source="CISA KEV",
                        title=vuln.get("cveID"),
                        content=f"{vuln.get('vulnerabilityName')} - {vuln.get('shortDescription')}",
                        threat_type="vulnerability",
                        severity="critical",
                        confidence_score=1.0,
                        published_date=datetime.strptime(vuln.get("dateAdded"), "%Y-%m-%d") if vuln.get("dateAdded") else None,
                        ingested_at=datetime.utcnow()
                    )
                    db.add(threat_intel)
                    ingested_count += 1

                if ingested_count % 50 == 0:
                    db.commit()

            except Exception as e:
                print(f"ERROR ingesting CISA KEV entry: {e}")
                continue

        db.commit()
        self.last_update = datetime.utcnow()
        print(f"CISA KEV: Ingested {ingested_count} new threat intelligence items")
        return ingested_count

    async def analyze_threat_relevance(
        self,
        db: Session,
        asset_id: int
    ) -> List[Dict]:
        asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
        if not asset:
            return []

        relevant_threats = []

        threats = db.query(models.ThreatIntel).filter(
            models.ThreatIntel.threat_type == "vulnerability",
            models.ThreatIntel.severity.in_(["critical", "high"])
        ).order_by(models.ThreatIntel.published_date.desc()).limit(100).all()

        for threat in threats:
            relevance_score = 0.0
            reasons = []

            if asset.os_version:
                if any(keyword in asset.os_version.lower() for keyword in ["windows", "linux", "ubuntu"]):
                    if any(keyword in threat.content.lower() for keyword in ["windows", "linux", "ubuntu"]):
                        relevance_score += 0.3
                        reasons.append("OS type match")

            asset_vulns = db.query(models.Vulnerability).filter(
                models.Vulnerability.asset_id == asset_id
            ).all()

            for vuln in asset_vulns:
                if vuln.cve_id and vuln.cve_id in threat.title:
                    relevance_score += 0.5
                    reasons.append(f"Direct CVE match: {vuln.cve_id}")

            if relevance_score > 0:
                relevant_threats.append({
                    "threat_id": threat.id,
                    "cve_id": threat.title,
                    "description": threat.content,
                    "severity": threat.severity,
                    "relevance_score": min(relevance_score, 1.0),
                    "reasons": reasons,
                    "published_date": threat.published_date.isoformat() if threat.published_date else None
                })

        relevant_threats.sort(key=lambda x: x["relevance_score"], reverse=True)
        return relevant_threats[:20]

    async def get_emerging_threats(self, db: Session, days: int = 7) -> List[Dict]:
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        threats = db.query(models.ThreatIntel).filter(
            models.ThreatIntel.published_date >= cutoff_date,
            models.ThreatIntel.severity.in_(["critical", "high"])
        ).order_by(models.ThreatIntel.published_date.desc()).limit(50).all()

        return [
            {
                "id": t.id,
                "source": t.source,
                "title": t.title,
                "content": t.content,
                "severity": t.severity,
                "published_date": t.published_date.isoformat() if t.published_date else None,
                "confidence": float(t.confidence_score) if t.confidence_score else 0.0
            }
            for t in threats
        ]

    async def should_update(self) -> bool:
        if not self.last_update:
            return True
        return datetime.utcnow() - self.last_update > self.update_interval

threat_intel_service = ThreatIntelligenceService()
