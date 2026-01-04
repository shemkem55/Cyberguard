from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..audit_trail import audit_trail

router = APIRouter()

@router.get("/audit/recent")
async def get_recent_audit_entries(limit: int = 50, db: Session = Depends(get_db)):
    """Retrieve recent audit trail entries"""
    entries = audit_trail.get_recent_entries(limit=limit)
    return {
        "total": len(entries),
        "entries": entries
    }

@router.get("/audit/summary")
async def get_governance_summary(db: Session = Depends(get_db)):
    """Get a summary of governance decisions"""
    summary = audit_trail.get_governance_summary()
    return summary

@router.get("/audit/by-category/{category}")
async def get_entries_by_category(category: str, limit: int = 50, db: Session = Depends(get_db)):
    """Query audit entries by action category"""
    entries = audit_trail.query_by_action_category(category, limit=limit)
    return {
        "category": category,
        "total": len(entries),
        "entries": entries
    }
