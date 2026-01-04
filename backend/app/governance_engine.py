
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime

class ActionCategory(Enum):
    """Classification of AI-proposed actions"""
    INFORMATIONAL = "informational"  # Just providing information (safe)
    ANALYSIS = "analysis"  # Analyzing data (safe)
    RECOMMENDATION = "recommendation"  # Suggesting actions (safe)
    SIMULATION = "simulation"  # Running simulations (requires approval)
    CONFIGURATION_CHANGE = "configuration_change"  # Modifying settings (requires approval)
    REMEDIATION = "remediation"  # Applying fixes (requires approval)
    SCAN_EXECUTION = "scan_execution"  # Running scans (requires approval)
    BLOCKED = "blocked"  # Explicitly prohibited

class DecisionBoundary:
    """Defines what AI can and cannot do"""
    
    # Actions the AI can perform autonomously
    AUTONOMOUS_ACTIONS = {
        ActionCategory.INFORMATIONAL,
        ActionCategory.ANALYSIS,
        ActionCategory.RECOMMENDATION
    }
    
    # Actions that require human approval
    APPROVAL_REQUIRED = {
        ActionCategory.SIMULATION,
        ActionCategory.CONFIGURATION_CHANGE,
        ActionCategory.REMEDIATION,
        ActionCategory.SCAN_EXECUTION
    }
    
    # Actions that are explicitly prohibited
    PROHIBITED_ACTIONS = {
        ActionCategory.BLOCKED
    }
    
    @staticmethod
    def classify_action(intent: str, message: str) -> ActionCategory:
        """
        Classify an action based on intent and message content.
        This determines whether human approval is needed.
        """
        message_lower = message.lower()
        
        # Prohibited actions (exploit generation, unauthorized access)
        if any(keyword in message_lower for keyword in [
            "exploit", "hack", "crack password", "bypass authentication",
            "ddos", "malware", "backdoor"
        ]):
            return ActionCategory.BLOCKED
        
        # Approval-required actions
        if intent == "SCAN_REQUEST":
            return ActionCategory.SCAN_EXECUTION
        
        if any(keyword in message_lower for keyword in ["fix", "patch", "remediate", "apply"]):
            return ActionCategory.REMEDIATION
        
        if any(keyword in message_lower for keyword in ["configure", "change settings", "modify"]):
            return ActionCategory.CONFIGURATION_CHANGE
        
        if any(keyword in message_lower for keyword in ["simulate", "test attack", "penetration test"]):
            return ActionCategory.SIMULATION
        
        # Analysis actions (safe)
        if intent in ["LIST_VULNERABILITIES", "VULN_EXPLANATION"]:
            return ActionCategory.ANALYSIS
        
        # Recommendations (safe)
        if intent == "REMEDIATION_ADVICE":
            return ActionCategory.RECOMMENDATION
        
        # Default to informational
        return ActionCategory.INFORMATIONAL
    
    @staticmethod
    def requires_approval(action_category: ActionCategory) -> bool:
        """Check if an action requires human approval"""
        return action_category in DecisionBoundary.APPROVAL_REQUIRED
    
    @staticmethod
    def is_prohibited(action_category: ActionCategory) -> bool:
        """Check if an action is prohibited"""
        return action_category in DecisionBoundary.PROHIBITED_ACTIONS


class GovernanceEngine:
    """
    Enforces safety and compliance policies.
    Ensures the AI operates within authorized boundaries.
    """
    
    def __init__(self):
        self.decision_boundary = DecisionBoundary()
    
    def evaluate_action(
        self, 
        intent: str, 
        message: str,
        user_role: str
    ) -> Dict:
        """
        Evaluate whether an action is allowed, requires approval, or is blocked.
        
        Returns:
            {
                "allowed": bool,
                "action_category": str,
                "requires_approval": bool,
                "reason": str,
                "governance_note": str
            }
        """
        # Classify the action
        action_category = self.decision_boundary.classify_action(intent, message)
        
        # Check if prohibited
        if self.decision_boundary.is_prohibited(action_category):
            return {
                "allowed": False,
                "action_category": action_category.value,
                "requires_approval": False,
                "reason": "This action is explicitly prohibited by safety policies.",
                "governance_note": "BLOCKED: Request violates safety guidelines."
            }
        
        # Check if approval required
        requires_approval = self.decision_boundary.requires_approval(action_category)
        
        if requires_approval:
            return {
                "allowed": True,
                "action_category": action_category.value,
                "requires_approval": True,
                "reason": f"This action ({action_category.value}) requires human approval before execution.",
                "governance_note": f"APPROVAL REQUIRED: {action_category.value} must be reviewed by {user_role}."
            }
        
        # Autonomous action (safe)
        return {
            "allowed": True,
            "action_category": action_category.value,
            "requires_approval": False,
            "reason": "This action can be performed autonomously.",
            "governance_note": f"AUTONOMOUS: {action_category.value} is within AI authority."
        }
    
    def generate_refusal_message(self, action_category: ActionCategory) -> str:
        """Generate a professional refusal message"""
        return f"""
**Access Denied**

I cannot proceed with this request as it falls under the category: **{action_category.value}**.

**Reason**: This action violates CyberGuard's safety and authorization policies.

**Guidance**: 
- If you need to perform security testing, please use authorized penetration testing tools with proper approval.
- For vulnerability assessments, I can provide analysis and recommendations instead.
- Contact your security administrator for actions requiring elevated privileges.

**Compliance Note**: This restriction is in place to ensure regulatory compliance and system integrity.
        """.strip()
    
    def generate_approval_request_message(
        self, 
        action_category: ActionCategory,
        user_role: str
    ) -> str:
        """Generate a professional approval request message"""
        return f"""
**Approval Required**

The requested action is classified as: **{action_category.value}**

**Authorization**: This action requires explicit approval from a {user_role} or higher authority.

**Next Steps**:
1. Review the proposed action details below
2. Approve or deny the request via the Approval Manager
3. Once approved, I will proceed with execution

**Compliance**: This checkpoint ensures audit trail completeness and prevents unauthorized changes.
        """.strip()

# Singleton instance
governance_engine = GovernanceEngine()
