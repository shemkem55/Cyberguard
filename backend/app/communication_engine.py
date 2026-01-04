
from typing import Dict, List
from enum import Enum

class ResponsePattern(Enum):
    """Standard response structures for professional communication"""
    EXECUTIVE_SUMMARY = "executive_summary"  # High-level → Key points → Recommendation
    TECHNICAL_ANALYSIS = "technical_analysis"  # Issue → Root cause → Fix → Verification
    STEP_BY_STEP = "step_by_step"  # Steps with clear progression
    RISK_ASSESSMENT = "risk_assessment"  # Risk → Impact → Mitigation
    SIMPLE_ANSWER = "simple_answer"  # Direct, concise response

class CommunicationEngine:
    """
    Enforces elite-level communication standards.
    Ensures responses are calm, precise, and professionally structured.
    """
    
    def __init__(self):
        self.tone_rules = self._initialize_tone_rules()
        self.response_templates = self._initialize_templates()
    
    def _initialize_tone_rules(self) -> Dict:
        """Define professional communication standards"""
        return {
            "forbidden_phrases": [
                "absolutely must", "guaranteed", "100% certain", "never fails",
                "hack", "exploit", "break into", "pwn", "owned",
                "revolutionary", "game-changing", "cutting-edge" # Avoid hype
            ],
            "preferred_language": {
                "hack": "assess",
                "exploit": "validate vulnerability",
                "attack": "security test",
                "break": "identify weakness in",
                "guaranteed": "highly likely",
                "never": "rarely",
                "always": "typically"
            },
            "uncertainty_phrases": [
                "Based on available data",
                "In most cases",
                "According to industry standards",
                "It is recommended that",
                "Evidence suggests",
                "Typically"
            ]
        }
    
    def _initialize_templates(self) -> Dict:
        """Define professional response templates"""
        return {
            ResponsePattern.EXECUTIVE_SUMMARY: """
**EXECUTIVE SUMMARY**
{summary}

**KEY FINDINGS**
{key_findings}

**RECOMMENDED ACTION**
{recommendation}
""".strip(),
            
            ResponsePattern.TECHNICAL_ANALYSIS: """
**ISSUE IDENTIFIED**
{issue}

**ROOT CAUSE**
{root_cause}

**RECOMMENDED FIX**
{fix}

**VERIFICATION STEPS**
{verification}
""".strip(),
            
            ResponsePattern.STEP_BY_STEP: """
**PROCEDURE**

{steps}

**IMPORTANT NOTES**
{notes}
""".strip(),
            
            ResponsePattern.RISK_ASSESSMENT: """
**RISK OVERVIEW**
{risk_description}

**POTENTIAL IMPACT**
{impact}

**MITIGATION STRATEGY**
{mitigation}

**PRIORITY**: {priority}
""".strip()
        }
    
    def format_response(
        self, 
        raw_response: str, 
        pattern: ResponsePattern,
        user_role: str,
        intent: str
    ) -> str:
        """
        Format a response according to professional standards.
        Applies role-specific tone and structure.
        """
        # Apply tone calibration
        calibrated_response = self._calibrate_tone(raw_response)
        
        # Apply role-specific formatting
        if user_role == "Executive":
            return self._format_for_executive(calibrated_response, intent)
        elif user_role == "Engineer":
            return self._format_for_engineer(calibrated_response, intent)
        else:  # Analyst
            return self._format_for_analyst(calibrated_response, intent)
    
    def _calibrate_tone(self, text: str) -> str:
        """
        Ensure professional, calm tone.
        Replace problematic language with appropriate alternatives.
        """
        calibrated = text
        
        # Replace forbidden phrases with professional alternatives
        for forbidden, preferred in self.tone_rules["preferred_language"].items():
            # Case-insensitive replacement
            import re
            pattern = re.compile(re.escape(forbidden), re.IGNORECASE)
            calibrated = pattern.sub(preferred, calibrated)
        
        return calibrated
    
    def _format_for_executive(self, response: str, intent: str) -> str:
        """
        Executive format: High-level summary → Business impact → Action
        """
        # Add executive framing
        prefix = "**Executive Summary**\n\n"
        
        # Ensure business language (not too technical)
        if "CVE-" in response and "business impact" not in response.lower():
            response += "\n\n*Note: This technical finding may impact system availability and data security.*"
        
        return prefix + response
    
    def _format_for_engineer(self, response: str, intent: str) -> str:
        """
        Engineer format: Technical detail → Code examples → Verification
        """
        # Engineers want specifics
        if intent == "REMEDIATION_ADVICE" and "```" not in response:
            # Suggest adding code if missing
            response += "\n\n*For code-level implementation, specify your framework (Django, Flask, etc.) for detailed examples.*"
        
        return response
    
    def _format_for_analyst(self, response: str, intent: str) -> str:
        """
        Analyst format: Balanced - context + technical + actionable
        """
        # Analysts get the balanced view
        return response
    
    def generate_conversation_discipline_prompt(self, intent: str) -> str:
        """
        Provide guidance on when to ask clarifying questions vs provide answers.
        """
        discipline_rules = {
            "GENERAL_CHAT": "Ask clarifying questions to understand what the user needs.",
            "SCAN_REQUEST": "Confirm scope and authorization before proceeding.",
            "REMEDIATION_ADVICE": "Provide direct guidance. Only ask for clarification on framework/version.",
            "VULN_EXPLANATION": "Provide explanation directly. No need to ask questions unless CVE ID is ambiguous.",
            "LIST_VULNERABILITIES": "Provide the list directly from context. No questions needed.",
            "REPORT_GENERATION": "Confirm report format preferences (PDF, HTML, JSON) if not specified."
        }
        
        return discipline_rules.get(intent, "Respond directly and professionally.")
    
    def should_ask_clarification(self, message: str, context: str, intent: str) -> bool:
        """
        Determine if the AI should ask for clarification vs provide a direct answer.
        """
        # Ask for clarification if:
        # 1. Request is ambiguous
        # 2. Missing critical context (e.g., which asset?)
        # 3. Safety-critical action without explicit scope
        
        ask_clarification = []
        
        # Check for ambiguity
        ambiguous_keywords = ["this", "that", "it", "the thing", "the issue"]
        if any(keyword in message.lower() for keyword in ambiguous_keywords) and not context:
            ask_clarification.append("Request is ambiguous without context")
        
        # Check for missing scope in scan requests
        if intent == "SCAN_REQUEST" and "target" not in message.lower() and not context:
            ask_clarification.append("Scan target not specified")
        
        return len(ask_clarification) > 0
    
    def generate_professional_sign_off(self, user_role: str, requires_approval: bool) -> str:
        """Generate a professional closing statement"""
        if requires_approval:
            return "\n\n---\n*This action requires authorization. Please review and approve before execution.*"
        
        role_sign_offs = {
            "Executive": "\n\n---\n*For detailed technical analysis, consult with your security engineering team.*",
            "Engineer": "\n\n---\n*Validate in a test environment before applying to production.*",
            "Analyst": "\n\n---\n*Let me know if you need additional analysis or remediation steps.*"
        }
        
        return role_sign_offs.get(user_role, "")

# Singleton instance
communication_engine = CommunicationEngine()
