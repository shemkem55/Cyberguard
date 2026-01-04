from .core_ai import CoreAI
from .intent_engine import IntentEngine
from .strategy_engine import StrategyEngine
from .reasoning_engine import ReasoningEngine

class AIService:
    def __init__(self):
        self.core = CoreAI()
        self.intent_engine = IntentEngine(self.core)
        self.strategy_engine = StrategyEngine()
        self.reasoning_engine = ReasoningEngine(self.core)

    async def chat_response(self, message: str, context: str = "", history: list = None, user_role: str = "Analyst"):
        if history is None: history = []
        
        # 1. Orchestration Phase: Intent
        intent = await self.intent_engine.classify_intent(message)
        print(f"[Orchestrator] Intent: {intent}")
        
        # 2. Orchestration Phase: Strategy
        strategy = self.strategy_engine.determine_strategy(intent, context, user_role)
        print(f"[Orchestrator] Strategy: {strategy}")
        
        # 3. Reasoning Phase (Pillar 2: Deep Intelligence)
        # The AI thinks before it answers.
        print("[Orchestrator] Engaging Reasoning Engine...")
        reasoning_trace = await self.reasoning_engine.analyze(message, context, intent)
        print(f"[Reasoning Trace]: {reasoning_trace[:100]}...")
        
        # 4. Execution Phase: Response Generation
        # Construct the enterprise prompt stack including the reasoning trace
        system_prompt = self._build_enterprise_prompt(intent, context, history, user_role, strategy, reasoning_trace)
        
        response_text = await self.core.generate_response(system_prompt, message)
        
        return {"response": response_text, "intent": intent}
        
    def _build_enterprise_prompt(self, intent, context, history, user_role, strategy, reasoning_trace):
        # [Identity Layer]
        identity = """
        You are CyberGuard-AI, an advanced cybersecurity assistant for enterprise.
        Prioritize accuracy, safety, and role-appropriate communication.
        """
        
        # [Safety Layer]
        safety = """
        SAFETY:
        - No exploit generation.
        - No PII/Credential leakage.
        - Explicitly refuse unauthorized dangerous actions.
        """
        
        # [Context Layer]
        history_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in history[-3:]])
        context_block = f"SYSTEM CONTEXT:\n{context}\n\nHISTORY:\n{history_text}"
        
        # [Reasoning Injection]
        # We rely on the internal reasoning to guide the final answer
        reasoning_block = f"""
        INTERNAL REASONING (Use this to guide your valid response):
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
        If tools are needed ({strategy['tools']}), mention them.
        """
        
        return f"{identity}\n\n{safety}\n\n{context_block}\n\n{reasoning_block}\n\n{instructions}"

ai_service = AIService()
