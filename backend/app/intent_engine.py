
from langchain_core.prompts import ChatPromptTemplate
from .core_ai import CoreAI

class IntentEngine:
    def __init__(self, core_ai: CoreAI):
        self.core_ai = core_ai
        
    async def classify_intent(self, message: str) -> str:
        if self.core_ai.is_mock:
            if "scan" in message.lower(): return "SCAN_REQUEST"
            if "fix" in message.lower(): return "REMEDIATION_ADVICE"
            return "GENERAL_CHAT"
            
        prompt = """
        Classify the cybersecurity intent of this query into exactly one category:
        - GENERAL_CHAT
        - SCAN_REQUEST
        - VULN_EXPLANATION
        - REMEDIATION_ADVICE
        - REPORT_GENERATION
        - LIST_VULNERABILITIES
        
        Return ONLY the category name.
        """
        
        return await self.core_ai.generate_response(prompt, message)
