
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..ai_test_suite import ai_test_suite
from ..ai_service import ai_service

router = APIRouter()

@router.post("/testing/run-validation")
async def run_validation_tests(db: Session = Depends(get_db)):
    """
    Execute the AI validation test suite.
    Returns comprehensive test results.
    """
    report = await ai_test_suite.run_all_tests(ai_service)
    return report

@router.get("/testing/last-results")
async def get_last_test_results(db: Session = Depends(get_db)):
    """
    Get the results from the most recent test run.
    """
    if not ai_test_suite.results:
        return {"message": "No test results available. Run /testing/run-validation first."}
    
    report = ai_test_suite.generate_report()
    return report

@router.get("/testing/metrics")
async def get_testing_metrics(db: Session = Depends(get_db)):
    """
    Get high-level testing metrics for dashboard display.
    """
    if not ai_test_suite.results:
        return {
            "tests_run": 0,
            "pass_rate": 0,
            "safety_compliance": 0,
            "governance_compliance": 0
        }
    
    report = ai_test_suite.generate_report()
    
    return {
        "tests_run": report["summary"]["total_tests"],
        "pass_rate": report["summary"]["pass_rate"],
        "avg_execution_time": report["summary"]["avg_execution_time"],
        "safety_compliance": report["category_results"]["safety"]["pass_rate"],
        "governance_compliance": report["category_results"]["governance"]["pass_rate"],
        "accuracy_score": report["category_results"]["accuracy"]["pass_rate"],
        "communication_quality": report["category_results"]["communication"]["pass_rate"],
        "adversarial_resistance": report["category_results"]["adversarial"]["pass_rate"]
    }
