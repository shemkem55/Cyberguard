from .core_ai import CoreAI
from .intent_engine import IntentEngine
from .strategy_engine import StrategyEngine
from .reasoning_engine import ReasoningEngine
from .knowledge_graph import knowledge_graph
from .governance_engine import governance_engine
from .audit_trail import audit_trail

class AIService:
    def __init__(self):
        self.core = CoreAI()
        self.intent_engine = IntentEngine(self.core)
        self.strategy_engine = StrategyEngine()
        self.reasoning_engine = ReasoningEngine(self.core)
        self.knowledge = knowledge_graph
        self.governance = governance_engine
        self.audit = audit_trail

    async def chat_response(self, message: str, context: str = "", history: list = None, user_role: str = "Analyst"):
        if history is None: history = []
        
        # 1. Orchestration Phase: Intent
        intent = await self.intent_engine.classify_intent(message)
        print(f"[Orchestrator] Intent: {intent}")
        
        # 2. Governance Phase (Pillar 4: Safety & Authorization)
        # Evaluate whether this action is allowed BEFORE proceeding
        print("[Orchestrator] Evaluating Governance Policies...")
        governance_decision = self.governance.evaluate_action(intent, message, user_role)
        print(f"[Governance]: {governance_decision['governance_note']}")
        
        # Handle blocked actions (prohibited by policy)
        if not governance_decision["allowed"]:
            refusal_message = self.governance.generate_refusal_message(
                self.governance.decision_boundary.classify_action(intent, message)
            )
            
            # Log the blocked attempt to audit trail
            self.audit.log_decision(
                user_role=user_role,
                intent=intent,
                message=message,
                action_category=governance_decision["action_category"],
                governance_decision="BLOCKED",
                response_summary=refusal_message,
                knowledge_sources=[],
                reasoning_summary="Request violated safety policies."
            )
            
            return {
                "response": refusal_message,
                "intent": intent,
                "governance": governance_decision
            }
        
        # Handle approval-required actions
        if governance_decision["requires_approval"]:
            approval_message = self.governance.generate_approval_request_message(
                self.governance.decision_boundary.classify_action(intent, message),
                user_role
            )
            
            # Log the approval request
            self.audit.log_decision(
                user_role=user_role,
                intent=intent,
                message=message,
                action_category=governance_decision["action_category"],
                governance_decision="APPROVAL_REQUIRED",
                response_summary=approval_message,
                knowledge_sources=[],
                reasoning_summary="Action requires human authorization."
            )
            
            # Still provide analysis, but with approval notice
            response_with_notice = f"{approval_message}\n\n---\n\n**Analysis (for review):**\n\n"
        else:
            response_with_notice = ""
        
        # 3. Orchestration Phase: Strategy
        strategy = self.strategy_engine.determine_strategy(intent, context, user_role)
        print(f"[Orchestrator] Strategy: {strategy}")
        
        # 4. Knowledge Retrieval Phase (Pillar 3: Intellectual Rigor)
        print("[Orchestrator] Querying Knowledge Graph...")
        relevant_knowledge = self.knowledge.query_knowledge(
            query=message,
            min_confidence=0.5
        )
        print(f"[Knowledge]: Retrieved {len(relevant_knowledge)} items")
        knowledge_sources = [item['source'] for item in relevant_knowledge]
        
        # 5. Reasoning Phase (Pillar 2: Deep Intelligence)
        print("[Orchestrator] Engaging Reasoning Engine...")
        reasoning_trace = await self.reasoning_engine.analyze(message, context, intent)
        print(f"[Reasoning Trace]: {reasoning_trace[:100]}...")
        
        # 6. Execution Phase: Response Generation
        system_prompt = self._build_enterprise_prompt(
            intent, context, history, user_role, strategy, 
            reasoning_trace, relevant_knowledge, governance_decision
        )
        
        response_text = await self.core.generate_response(system_prompt, message)
        
        # Prepend approval notice if required
        final_response = response_with_notice + response_text
        
        # 7. Audit Trail (Pillar 4: Compliance & Accountability)
        self.audit.log_decision(
            user_role=user_role,
            intent=intent,
            message=message,
            action_category=governance_decision["action_category"],
            governance_decision=governance_decision["governance_note"],
            response_summary=final_response,
            knowledge_sources=knowledge_sources,
            reasoning_summary=reasoning_trace[:150]
        )
        print(f"[Audit] Decision logged: {governance_decision['action_category']}")
        
        return {
            "response": final_response,
            "intent": intent,
            "governance": governance_decision
        }
        
    def _build_enterprise_prompt(self, intent, context, history, user_role, strategy, reasoning_trace, knowledge_items, governance_decision):
        # [Identity Layer]
        identity = """
        You are CyberGuard-AI, an advanced cybersecurity assistant for enterprise.
        Prioritize accuracy, safety, and role-appropriate communication.
        You are powered by a verified knowledge base with source attribution.
        """
        
        # [Safety Layer]
        safety = """
        SAFETY:
        - No exploit generation.
        - No PII/Credential leakage.
        - Explicitly refuse unauthorized dangerous actions.
        """
        
        # [Governance Layer] - Pillar 4: Authorization Context
        governance_block = f"""
        GOVERNANCE CONTEXT:
        Action Category: {governance_decision['action_category']}
        Authorization Status: {governance_decision['governance_note']}
        User Role: {user_role}
        
        If this requires approval, provide analysis but clearly state execution is pending authorization.
        """
        
        # [Knowledge Layer] - Pillar 3: Institutional Knowledge
        knowledge_block = "KNOWLEDGE BASE (Use these verified sources):\n"
        if knowledge_items:
            for idx, item in enumerate(knowledge_items[:5], 1):
                knowledge_block += f"\n[{idx}] {item['content']}\n"
                knowledge_block += f"    Type: {item['type']} | Source: {item['source']} | Confidence: {item['confidence']}\n"
        else:
            knowledge_block += "  No specific knowledge items found. Use general cybersecurity principles.\n"
        
        # [Context Layer]
        history_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in history[-3:]])
        context_block = f"SYSTEM CONTEXT:\n{context}\n\nHISTORY:\n{history_text}"
        
        # [Reasoning Injection]
        reasoning_block = f"""
        INTERNAL REASONING (Use this to guide your response):
        {reasoning_trace}
        """
        
        # [Instruction Layer]
        instructions = f"""
        USER ROLE: {user_role}
        STRATEGY:
        - Style: {strategy['style']}
        - Format: {strategy['format']}
        - Depth: {strategy['depth']}
        
        TASK:
        Address the user's intent [{intent}].
        When referencing knowledge, cite the source (e.g., "According to OWASP...").
        If tools are needed ({strategy['tools']}), mention them.
        """
        
        return f"{identity}\n\n{safety}\n\n{governance_block}\n\n{knowledge_block}\n\n{context_block}\n\n{reasoning_block}\n\n{instructions}"

ai_service = AIService()


