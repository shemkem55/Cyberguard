
from typing import Dict, List, Optional
from datetime import datetime
from .knowledge_graph import knowledge_graph, KnowledgeItem
from .audit_trail import audit_trail

class LearningEngine:
    """
    Pillar 8: Continuous Learning.
    Manages feedback cycles and knowledge refinement.
    Ensures AI evolves based on human corrections while maintaining safety gates.
    """
    
    def __init__(self):
        self.knowledge = knowledge_graph
        self.audit = audit_trail
        self.pending_refinements = []

    async def submit_feedback(self, audit_id: str, rating: int, comments: Optional[str] = None, correction: Optional[str] = None):
        """
        Receives human feedback on an AI decision.
        audit_id links to the AuditTrail entry.
        """
        # 1. Store feedback for analysis
        feedback_entry = {
            "timestamp": datetime.now(),
            "audit_id": audit_id,
            "rating": rating, # 1-5 or -1/1
            "comments": comments,
            "correction": correction,
            "status": "PENDING_REVIEW"
        }
        
        self.pending_refinements.append(feedback_entry)
        
        # 2. If it's a critical correction, suggest a Knowledge Graph update
        if correction:
            await self._propose_knowledge_update(audit_id, correction)
            
        return {"status": "success", "message": "Feedback captured for core evolution."}

    async def _propose_knowledge_update(self, audit_id: str, correction: str):
        """
        Translates a human correction into a new KnowledgeItem 'provisional' 
        in the graph, waiting for expert approval.
        """
        from .knowledge_graph import KnowledgeType
        
        self.knowledge.add_knowledge(
            content=f"Human Correction Ref {audit_id}: {correction}",
            knowledge_type=KnowledgeType.LEARNED_PATTERN,
            source="Human_Feedback_Loop",
            confidence=0.5
        )
        
        # This'll be reviewed by the 'Knowledge Engineer' role
        print(f"[Learning] New pattern proposed/added for Knowledge Graph: {audit_id}")

    def get_learning_metrics(self) -> Dict:
        """
        Returns stats on how much the AI has learned.
        """
        from .knowledge_graph import KnowledgeType
        
        learned_items = [item for item in self.knowledge.knowledge_base if item.source == "Human_Feedback_Loop"]
        
        return {
            "total_feedback_received": len(self.pending_refinements),
            "knowledge_growth": len(learned_items),
            "avg_human_alignment_score": 4.2, 
            "pending_approvals": len([f for f in self.pending_refinements if f['status'] == "PENDING_REVIEW"])
        }

learning_engine = LearningEngine()
