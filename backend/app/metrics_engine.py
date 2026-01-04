
from typing import Dict, List
from datetime import datetime, timedelta
from .audit_trail import audit_trail
from .ai_test_suite import ai_test_suite

class MetricsEngine:
    """
    Aggregates data from AuditTrail and TestSuite to provide professional KPIs.
    Focuses on accuracy, trust, safety, and efficiency.
    """
    
    def __init__(self):
        self.audit = audit_trail
        self.test_suite = ai_test_suite

    def get_performance_kpis(self) -> Dict:
        """
        Calculates core performance metrics.
        """
        audit_summary = self.audit.get_governance_summary()
        test_report = self.test_suite.generate_report() if self.test_suite.results else None
        
        total_decisions = audit_summary.get("total_decisions", 0)
        
        # Calculate Human Override Frequency (simulated based on approval logs)
        approvals = audit_summary.get("by_governance_decision", {}).get("APPROVAL_REQUIRED", 0)
        # In a real system, we'd track Denied vs Approved in a separate table
        # For now, we estimate override rate from audit categories
        override_rate = (approvals / total_decisions * 100) if total_decisions > 0 else 0
        
        return {
            "reliability": {
                "test_pass_rate": test_report["summary"]["pass_rate"] if test_report else 0,
                "avg_accuracy_score": test_report["summary"]["avg_score"] if test_report else 0,
                "decision_reversal_rate": 2.5,  # Mocked: percentage of AI decisions overturned by humans
            },
            "safety": {
                "safety_compliance": test_report["category_results"]["safety"]["pass_rate"] if test_report else 0,
                "governance_compliance": test_report["category_results"]["governance"]["pass_rate"] if test_report else 0,
                "blocked_attempts_count": audit_summary.get("by_governance_decision", {}).get("BLOCKED", 0),
            },
            "efficiency": {
                "avg_response_time": test_report["summary"]["avg_execution_time"] if test_report else 0.5,
                "total_automated_decisions": total_decisions,
                "human_override_frequency": round(override_rate, 2),
            },
            "trust": {
                "user_trust_score": 4.8,  # Mocked: Out of 5 based on user feedback
                "false_positive_rate": 1.2, # Mocked: percentage of results marked as incorrect by users
            }
        }

    def get_time_series_data(self, days: int = 7) -> List[Dict]:
        """
        Generates daily activity data for charts.
        """
        now = datetime.now()
        series = []
        
        for i in range(days):
            date = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            # In a real system, we would query the database for daily counts
            # For this elite demo, we'll provide simulated trend data
            series.append({
                "date": date,
                "decisions": 10 + (i * 2),
                "accuracy": 94 + (i * 0.5),
                "safety_events": 1 if i % 2 == 0 else 0
            })
            
        return sorted(series, key=lambda x: x["date"])

metrics_engine = MetricsEngine()
