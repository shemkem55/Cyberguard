
from sqlalchemy.orm import Session
from app import models
from app.neo4j_service import neo4j_service
from sqlalchemy import or_

class KnowledgeService:
    def __init__(self):
        pass

    def retrieve_context(self, db: Session, query: str):
        """
        Retrieves relevant context from SQL and Graph based on user query.
        Phase 3 RAG Implementation.
        """
        context_parts = []
        
        # 1. Simple Keyword Extraction (Prototype)
        # In a real system, use an LLM to extract entities.
        # Here we look for asset names in the query.
        assets = db.query(models.Asset).all()
        matched_assets = []
        for asset in assets:
            if asset.name.lower() in query.lower() or asset.ip_address in query:
                matched_assets.append(asset)
        
        # 2. Retrieve Asset Details (if matched)
        if matched_assets:
            context_parts.append("\n--- RELEVANT ASSET DATA ---")
            for asset in matched_assets:
                context_parts.append(f"Asset: {asset.name} ({asset.type})")
                context_parts.append(f"  IP: {asset.ip_address}")
                context_parts.append(f"  Criticality: {asset.criticality}/10")
                context_parts.append(f"  OS: {asset.os_version}")
                
                # 3. Graph Context (GraphRAG)
                # "What is this asset connected to?"
                graph_data = neo4j_service.get_asset_context(asset.name)
                if graph_data:
                    context_parts.append(f"  Graph Connections ({len(graph_data)}):")
                    for rel in graph_data:
                        target = rel.get("name") or rel.get("cve_id")
                        context_parts.append(f"    - [{rel['rel']}] -> {target}")
        
        # 4. Vulnerability Search
        # If query mentions "vuln" or "cve", fetch high severity ones
        if "cve" in query.lower() or "vulnerab" in query.lower():
            vulns = db.query(models.Vulnerability).filter(models.Vulnerability.severity >= 7).limit(5).all()
            context_parts.append("\n--- CRITICAL VULNERABILITIES ---")
            for v in vulns:
                context_parts.append(f"{v.cve_id}: {v.title} (Severity: {v.severity})")
                
        # 5. Default Context (Fallback)
        if not context_parts:
             context_parts.append("\n--- GENERAL SYSTEM SUMMARY ---")
             total_assets = db.query(models.Asset).count()
             context_parts.append(f"Total Assets Managed: {total_assets}")
             
        return "\n".join(context_parts)

knowledge_service = KnowledgeService()
