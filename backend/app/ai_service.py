from typing import Dict
from .core_ai import CoreAI
from .intent_engine import IntentEngine
from .strategy_engine import StrategyEngine
from .reasoning_engine import ReasoningEngine
from .knowledge_graph import knowledge_graph
from .governance_engine import governance_engine
from .audit_trail import audit_trail
from .communication_engine import communication_engine, ResponsePattern

class AIService:
    def __init__(self):
        self.core = CoreAI()
        self.intent_engine = IntentEngine(self.core)
        self.strategy_engine = StrategyEngine()
        self.reasoning_engine = ReasoningEngine(self.core)
        self.knowledge = knowledge_graph
        self.governance = governance_engine
        self.audit = audit_trail
        self.communication = communication_engine

    async def chat_response(self, message: str, context: str = "", history: list = None, user_role: str = "Analyst"):
        if history is None: history = []
        
        # 1. Orchestration Phase: Intent
        intent = await self.intent_engine.classify_intent(message)
        print(f"[Orchestrator] Intent: {intent}")
        
        # 2. Governance Phase (Pillar 4: Safety & Authorization)
        print("[Orchestrator] Evaluating Governance Policies...")
        governance_decision = self.governance.evaluate_action(intent, message, user_role)
        print(f"[Governance]: {governance_decision['governance_note']}")
        
        # Handle blocked actions
        if not governance_decision["allowed"]:
            refusal_message = self.governance.generate_refusal_message(
                self.governance.decision_boundary.classify_action(intent, message)
            )
            
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
            
            response_with_notice = f"{approval_message}\n\n---\n\n**Analysis (for review):**\n\n"
        else:
            response_with_notice = ""
        
        # 3. Orchestration Phase: Strategy
        strategy = self.strategy_engine.determine_strategy(intent, context, user_role)
        print(f"[Orchestrator] Strategy: {strategy}")
        
        # 4. Knowledge Retrieval Phase (Pillar 3)
        print("[Orchestrator] Querying Knowledge Graph...")
        relevant_knowledge = self.knowledge.query_knowledge(
            query=message,
            min_confidence=0.5
        )
        print(f"[Knowledge]: Retrieved {len(relevant_knowledge)} items")
        knowledge_sources = [item['source'] for item in relevant_knowledge]
        
        # 5. Reasoning Phase (Pillar 2)
        print("[Orchestrator] Engaging Reasoning Engine...")
        reasoning_trace = await self.reasoning_engine.analyze(message, context, intent)
        print(f"[Reasoning Trace]: {reasoning_trace[:100]}...")
        
        # 6. Communication Discipline (Pillar 5)
        # Determine if we should ask clarifying questions
        should_clarify = self.communication.should_ask_clarification(message, context, intent)
        conversation_discipline = self.communication.generate_conversation_discipline_prompt(intent)
        
        print(f"[Communication]: Discipline = {conversation_discipline[:50]}...")
        
        # 7. Execution Phase: Response Generation
        system_prompt = self._build_enterprise_prompt(
            intent, context, history, user_role, strategy, 
            reasoning_trace, relevant_knowledge, governance_decision,
            conversation_discipline
        )
        
        response_text = await self.core.generate_response(system_prompt, message)
        
        # 8. Communication Polish (Pillar 5: Elite-Level Chat)
        # Apply tone calibration and professional formatting
        print("[Communication] Applying tone calibration...")
        polished_response = self.communication.format_response(
            raw_response=response_text,
            pattern=self._determine_response_pattern(intent, strategy),
            user_role=user_role,
            intent=intent
        )
        
        # Add professional sign-off
        sign_off = self.communication.generate_professional_sign_off(
            user_role=user_role,
            requires_approval=governance_decision["requires_approval"]
        )
        polished_response += sign_off
        
        # Prepend approval notice if required
        final_response = response_with_notice + polished_response
        
        # 9. Audit Trail (Pillar 4)
        audit_entry = self.audit.log_decision(
            user_role=user_role,
            intent=intent,
            message=message,
            action_category=governance_decision["action_category"],
            governance_decision=governance_decision["governance_note"],
            response_summary=final_response,
            knowledge_sources=knowledge_sources,
            reasoning_summary=reasoning_trace[:150]
        )
        print(f"[Audit] Decision logged: {governance_decision['action_category']} (ID: {audit_entry.id})")
        
        return {
            "response": final_response,
            "intent": intent,
            "governance": governance_decision,
            "audit_id": audit_entry.id
        }
    
    def _determine_response_pattern(self, intent: str, strategy: Dict) -> ResponsePattern:
        """Map intent and strategy to appropriate response pattern"""
        if intent == "REMEDIATION_ADVICE":
            return ResponsePattern.STEP_BY_STEP
        elif intent == "VULN_EXPLANATION":
            return ResponsePattern.TECHNICAL_ANALYSIS
        elif intent == "LIST_VULNERABILITIES":
            return ResponsePattern.RISK_ASSESSMENT
        elif intent == "REPORT_GENERATION":
            return ResponsePattern.EXECUTIVE_SUMMARY
        else:
            return ResponsePattern.SIMPLE_ANSWER
        
    def _build_enterprise_prompt(self, intent, context, history, user_role, strategy, reasoning_trace, knowledge_items, governance_decision, conversation_discipline):
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
        
        # [Communication Standards Layer] - Pillar 5: Elite-Level Chat
        communication_standards = f"""
        COMMUNICATION EXCELLENCE:
        - Tone: Calm, precise, conservative (never overconfident or speculative)
        - Language: Professional (avoid "hack", "exploit", "guaranteed")
        - Uncertainty: Explicitly state when uncertain ("Based on available data...", "Typically...")
        - Conversation Discipline: {conversation_discipline}
        - Structure: Clear sections with headers for readability
        - Citations: Reference sources (e.g., "According to OWASP Top 10...")
        
        FORBIDDEN LANGUAGE:
        - "100% certain", "guaranteed", "never fails"
        - "hack", "exploit", "break into", "pwn"
        - "revolutionary", "game-changing" (no hype)
        
        PREFERRED ALTERNATIVES:
        - "assess" instead of "hack"
        - "validate vulnerability" instead of "exploit"
        - "security test" instead of "attack"
        - "highly likely" instead of "guaranteed"
        """
        
        # [Governance Layer]
        governance_block = f"""
        GOVERNANCE CONTEXT:
        Action Category: {governance_decision['action_category']}
        Authorization Status: {governance_decision['governance_note']}
        User Role: {user_role}
        
        If this requires approval, provide analysis but clearly state execution is pending authorization.
        """
        
        # [Knowledge Layer]
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
        
        Respond in a calm, professional manner appropriate for a senior security advisor.
        """
        
        return f"{identity}\n\n{safety}\n\n{communication_standards}\n\n{governance_block}\n\n{knowledge_block}\n\n{context_block}\n\n{reasoning_block}\n\n{instructions}"

ai_service = AIService()



