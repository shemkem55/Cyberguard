
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..metrics_engine import metrics_engine

router = APIRouter()

@router.get("/metrics/kpis")
async def get_kpis():
    """Get high-level professional KPIs for the dashboard"""
    return metrics_engine.get_performance_kpis()

@router.get("/metrics/activity")
async def get_activity_trends(days: int = 7):
    """Get activity trends for charting"""
    return metrics_engine.get_time_series_data(days=days)

@router.get("/metrics/trust-feedback")
async def get_trust_feedback():
    """Get detailed user trust and feedback metrics"""
    kpis = metrics_engine.get_performance_kpis()
    return kpis["trust"]
