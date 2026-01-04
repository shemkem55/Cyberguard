
from datetime import datetime
from typing import Dict, List, Optional
import json
from pathlib import Path

import uuid

class AuditEntry:
    """Represents a single audit trail entry"""
    
    def __init__(
        self,
        timestamp: datetime,
        user_role: str,
        intent: str,
        message: str,
        action_category: str,
        governance_decision: str,
        response_summary: str,
        knowledge_sources: List[str] = None,
        reasoning_summary: str = ""
    ):
        self.id = str(uuid.uuid4())
        self.timestamp = timestamp
        self.user_role = user_role
        self.intent = intent
        self.message = message
        self.action_category = action_category
        self.governance_decision = governance_decision
        self.response_summary = response_summary
        self.knowledge_sources = knowledge_sources or []
        self.reasoning_summary = reasoning_summary
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "user_role": self.user_role,
            "intent": self.intent,
            "message": self.message[:100] + "..." if len(self.message) > 100 else self.message,
            "action_category": self.action_category,
            "governance_decision": self.governance_decision,
            "response_summary": self.response_summary[:200] + "..." if len(self.response_summary) > 200 else self.response_summary,
            "knowledge_sources": self.knowledge_sources,
            "reasoning_summary": self.reasoning_summary[:150] + "..." if len(self.reasoning_summary) > 150 else self.reasoning_summary
        }


class AuditTrail:
    """
    Maintains an immutable, append-only audit log of all AI decisions.
    Critical for compliance, security reviews, and incident investigation.
    """
    
    def __init__(self, log_file: str = "audit_trail.jsonl"):
        self.log_file = Path(log_file)
        self.in_memory_cache: List[AuditEntry] = []
        
    def log_decision(
        self,
        user_role: str,
        intent: str,
        message: str,
        action_category: str,
        governance_decision: str,
        response_summary: str,
        knowledge_sources: List[str] = None,
        reasoning_summary: str = ""
    ):
        """
        Log an AI decision with full context.
        This creates an immutable record for audit purposes.
        """
        entry = AuditEntry(
            timestamp=datetime.now(),
            user_role=user_role,
            intent=intent,
            message=message,
            action_category=action_category,
            governance_decision=governance_decision,
            response_summary=response_summary,
            knowledge_sources=knowledge_sources,
            reasoning_summary=reasoning_summary
        )
        
        # Add to in-memory cache
        self.in_memory_cache.append(entry)
        
        # Write to persistent log (append-only)
        self._write_to_log(entry)
        
        return entry
    
    def _write_to_log(self, entry: AuditEntry):
        """Write entry to JSONL file (append-only, immutable)"""
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(entry.to_dict()) + '\n')
        except Exception as e:
            print(f"[AUDIT WARNING] Failed to write audit log: {e}")
    
    def get_recent_entries(self, limit: int = 50) -> List[Dict]:
        """Retrieve recent audit entries for review"""
        return [entry.to_dict() for entry in self.in_memory_cache[-limit:]]
    
    def query_by_action_category(self, category: str, limit: int = 50) -> List[Dict]:
        """Query audit log by action category"""
        matching = [
            entry.to_dict() 
            for entry in self.in_memory_cache 
            if entry.action_category == category
        ]
        return matching[-limit:]
    
    def get_governance_summary(self) -> Dict:
        """Generate a summary of governance decisions"""
        total = len(self.in_memory_cache)
        if total == 0:
            return {"total_decisions": 0}
        
        by_category = {}
        by_decision = {}
        
        for entry in self.in_memory_cache:
            by_category[entry.action_category] = by_category.get(entry.action_category, 0) + 1
            by_decision[entry.governance_decision] = by_decision.get(entry.governance_decision, 0) + 1
        
        return {
            "total_decisions": total,
            "by_action_category": by_category,
            "by_governance_decision": by_decision,
            "latest_timestamp": self.in_memory_cache[-1].timestamp.isoformat() if self.in_memory_cache else None
        }

# Singleton instance
audit_trail = AuditTrail()
