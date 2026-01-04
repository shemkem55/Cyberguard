
from langchain_core.prompts import ChatPromptTemplate
from .core_ai import CoreAI

class IntentEngine:
    def __init__(self, core_ai: CoreAI):
        self.core_ai = core_ai
        
    async def classify_intent(self, message: str) -> str:
        if self.core_ai.is_mock:
            m = message.lower()
            if any(k in m for k in ["scan", "enumerate", "discover", "nmap"]): return "SCAN_REQUEST"
            if any(k in m for k in ["fix", "patch", "remediate", "mitigate"]): return "REMEDIATION_ADVICE"
            if any(k in m for k in ["why", "explain", "describe", "what is"]): return "VULN_EXPLANATION"
            if any(k in m for k in ["list", "show", "get vulnerabilities"]): return "LIST_VULNERABILITIES"
            if any(k in m for k in ["report", "generate", "summary"]): return "REPORT_GENERATION"
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
