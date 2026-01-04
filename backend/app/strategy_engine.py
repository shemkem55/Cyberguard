
class StrategyEngine:
    def determine_strategy(self, intent: str, context: str, user_role: str):
        strategy = {
            "style": "professional and direct",
            "format": "text",
            "depth": "summary",
            "tools": []
        }
        
        # Role Adaptation
        if user_role == "Executive":
            strategy["style"] = "strategic and concise"
            strategy["depth"] = "high-level summary"
        elif user_role == "Engineer":
            strategy["style"] = "highly technical"
            strategy["depth"] = "detailed technical specifications"
            
        # Format Planning
        if intent == "LIST_VULNERABILITIES":
            strategy["format"] = "markdown_table"
        elif intent == "REMEDIATION_ADVICE":
            strategy["format"] = "step_by_step_list"
            strategy["depth"] = "implementation steps"
            
        # Tool Strategy
        if intent == "SCAN_REQUEST":
            strategy["tools"].append("trigger_scan")
            
        return strategy
