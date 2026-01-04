
from .core_ai import CoreAI

class ReasoningEngine:
    def __init__(self, core_ai: CoreAI):
        self.core_ai = core_ai

    async def analyze(self, message: str, context: str, intent: str) -> str:
        """
        Performs deep reasoning (Chain of Thought) before generating the final answer.
        This step ensures the AI 'thinks' before it 'speaks'.
        """
        if self.core_ai.is_mock:
            return "[Reasoning] Mock analysis: Query is safe. Context contains vulnerability data. Plan: Summarize findings."

        prompt = f"""
        You are the Internal Reasoning Module for a Cyber Security AI.
        Perform a deep analysis of the user query based on the system context.
        
        QUERY: {message}
        INTENT: {intent}
        
        CONTEXT:
        {context}
        
        INSTRUCTIONS:
        Output a structured reasoning trace (internal monologue) with these sections:
        
        1. [FACT OBSERVATION]
           - List specific assets, CVEs, or IPs found in the context.
           - Identify any missing critical information.
           
        2. [SECURITY ANALYSIS]
           - Assess the technical severity (High/Medium/Low).
           - Identify potential risks or business impacts.
           
        3. [SAFETY & POLICY CHECK]
           - Does this request violate safety guidelines (e.g. asking for exploits)?
           - Is the user authorized to see this data? (Assume yes if data is in context).
           
        4. [RESPONSE PLAN]
           - What is the best way to answer?
           - Should we allow or refuse the request?
           
        Provide ONLY this reasoning structure. Do not generate the final response to the user yet.
        """
        
        return await self.core_ai.generate_response(prompt, "Analyze this request.")
