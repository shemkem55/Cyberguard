
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum

class KnowledgeType(Enum):
    FACT = "fact"  # Verified, objective information (CVE data, scan results)
    BEST_PRACTICE = "best_practice"  # Industry-standard recommendations
    HEURISTIC = "heuristic"  # Experience-based rules of thumb
    LEARNED_PATTERN = "learned_pattern"  # System-observed correlations

class KnowledgeItem:
    def __init__(
        self, 
        content: str, 
        knowledge_type: KnowledgeType,
        source: str,
        timestamp: datetime = None,
        confidence: float = 1.0
    ):
        self.content = content
        self.knowledge_type = knowledge_type
        self.source = source
        self.timestamp = timestamp or datetime.now()
        self.base_confidence = confidence
        
    def get_current_confidence(self) -> float:
        """
        Apply knowledge decay: older information loses confidence.
        Facts decay slower than heuristics.
        """
        age_days = (datetime.now() - self.timestamp).days
        
        # Decay rates by knowledge type
        decay_rates = {
            KnowledgeType.FACT: 0.99,  # Very slow decay (0.01% per day)
            KnowledgeType.BEST_PRACTICE: 0.995,  # 0.5% per day
            KnowledgeType.HEURISTIC: 0.98,  # 2% per day
            KnowledgeType.LEARNED_PATTERN: 0.95  # 5% per day (fastest decay)
        }
        
        decay_rate = decay_rates.get(self.knowledge_type, 0.99)
        decayed_confidence = self.base_confidence * (decay_rate ** age_days)
        
        return max(0.1, decayed_confidence)  # Floor at 10%

class KnowledgeGraph:
    def __init__(self):
        self.knowledge_base: List[KnowledgeItem] = []
        self._initialize_core_knowledge()
        
    def _initialize_core_knowledge(self):
        """Seed the graph with foundational cybersecurity knowledge"""
        
        # FACTS (from CVE databases, scan results)
        self.add_knowledge(
            "SQL Injection (CWE-89) allows attackers to execute arbitrary SQL commands.",
            KnowledgeType.FACT,
            "MITRE CWE Database",
            confidence=1.0
        )
        
        self.add_knowledge(
            "CVE-2021-44228 (Log4Shell) is a critical remote code execution vulnerability in Apache Log4j.",
            KnowledgeType.FACT,
            "NIST NVD",
            confidence=1.0
        )
        
        # BEST PRACTICES (from NIST, OWASP, CIS)
        self.add_knowledge(
            "Use parameterized queries to prevent SQL injection attacks.",
            KnowledgeType.BEST_PRACTICE,
            "OWASP Top 10",
            confidence=0.95
        )
        
        self.add_knowledge(
            "Apply security patches within 30 days for critical vulnerabilities.",
            KnowledgeType.BEST_PRACTICE,
            "NIST Cybersecurity Framework",
            confidence=0.9
        )
        
        # HEURISTICS (experience-based)
        self.add_knowledge(
            "If a web server shows outdated software versions, it likely has unpatched vulnerabilities.",
            KnowledgeType.HEURISTIC,
            "Security Expert Observation",
            confidence=0.75
        )
        
        self.add_knowledge(
            "Assets with open port 22 (SSH) and weak credentials are high-value targets.",
            KnowledgeType.HEURISTIC,
            "Penetration Testing Experience",
            confidence=0.8
        )
        
    def add_knowledge(
        self, 
        content: str, 
        knowledge_type: KnowledgeType, 
        source: str,
        confidence: float = 1.0
    ):
        """Add a new knowledge item to the graph"""
        item = KnowledgeItem(content, knowledge_type, source, confidence=confidence)
        self.knowledge_base.append(item)
        
    def query_knowledge(
        self, 
        query: str, 
        knowledge_types: Optional[List[KnowledgeType]] = None,
        min_confidence: float = 0.3
    ) -> List[Dict]:
        """
        Retrieve relevant knowledge with source attribution and confidence.
        Returns structured knowledge items.
        """
        results = []
        
        for item in self.knowledge_base:
            # Filter by knowledge type if specified
            if knowledge_types and item.knowledge_type not in knowledge_types:
                continue
                
            # Simple relevance check (keyword matching)
            # In production, use embeddings or graph traversal
            if any(keyword.lower() in item.content.lower() for keyword in query.split()):
                current_confidence = item.get_current_confidence()
                
                if current_confidence >= min_confidence:
                    results.append({
                        "content": item.content,
                        "type": item.knowledge_type.value,
                        "source": item.source,
                        "confidence": round(current_confidence, 2),
                        "age_days": (datetime.now() - item.timestamp).days
                    })
        
        # Sort by confidence (highest first)
        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results
        
    def get_knowledge_summary(self) -> str:
        """Generate a summary of the knowledge base for context"""
        total = len(self.knowledge_base)
        by_type = {}
        
        for item in self.knowledge_base:
            ktype = item.knowledge_type.value
            by_type[ktype] = by_type.get(ktype, 0) + 1
            
        summary = f"Knowledge Base: {total} items\n"
        for ktype, count in by_type.items():
            summary += f"  - {ktype}: {count}\n"
            
        return summary

# Singleton instance
knowledge_graph = KnowledgeGraph()
