
from fastapi import APIRouter, Body
from typing import Optional
from .learning_engine import learning_engine

router = APIRouter()

@router.post("/learning/feedback")
async def submit_feedback(
    audit_id: str = Body(...),
    rating: int = Body(...),
    comments: Optional[str] = Body(None),
    correction: Optional[str] = Body(None)
):
    """Submit human feedback for AI response improvement"""
    return await learning_engine.submit_feedback(audit_id, rating, comments, correction)

@router.get("/learning/metrics")
async def get_learning_stats():
    """Get metrics on system's continuous learning progress"""
    return learning_engine.get_learning_metrics()

@router.get("/learning/pending")
async def get_pending_refinements():
    """Get data awaiting human approval for knowledge refinement"""
    return learning_engine.pending_refinements
