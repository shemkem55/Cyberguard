from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from .database import get_db
from .threat_intel_service import threat_intel_service

router = APIRouter()

@router.post("/threat-intel/ingest/cisa-kev")
async def ingest_cisa_kev(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Ingest CISA Known Exploited Vulnerabilities catalog.
    Runs in background to avoid blocking.
    """
    background_tasks.add_task(threat_intel_service.ingest_cisa_kev, db)

    return {
        "status": "started",
        "message": "CISA KEV ingestion started in background"
    }

@router.get("/threat-intel/emerging")
async def get_emerging_threats(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """
    Get emerging threats from the last N days.
    """
    threats = await threat_intel_service.get_emerging_threats(db, days=days)

    return {
        "count": len(threats),
        "days": days,
        "threats": threats
    }

@router.get("/threat-intel/relevance/{asset_id}")
async def analyze_threat_relevance(
    asset_id: int,
    db: Session = Depends(get_db)
):
    """
    Analyze threat intelligence relevance to a specific asset.
    Returns prioritized list of relevant threats.
    """
    relevant_threats = await threat_intel_service.analyze_threat_relevance(db, asset_id)

    return {
        "asset_id": asset_id,
        "relevant_threats_count": len(relevant_threats),
        "threats": relevant_threats
    }

@router.get("/threat-intel/status")
async def get_threat_intel_status():
    """
    Get threat intelligence service status.
    """
    should_update = await threat_intel_service.should_update()

    return {
        "last_update": threat_intel_service.last_update.isoformat() if threat_intel_service.last_update else None,
        "should_update": should_update,
        "update_interval_hours": threat_intel_service.update_interval.total_seconds() / 3600
    }
