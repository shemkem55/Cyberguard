
"""
AI System Test Runner
Run comprehensive validation tests on the AI system.
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ai_test_suite import ai_test_suite
from app.ai_service import ai_service

async def main():
    """Run the AI validation test suite"""
    print("\n🚀 Initializing AI Validation Tests...\n")
    
    # Run all tests
    report = await ai_test_suite.run_all_tests(ai_service)
    
    # Print detailed report
    ai_test_suite.print_report(report)
    
    # Exit code based on results
    if report["summary"]["pass_rate"] < 100:
        print("⚠️  Some tests failed. Review the report above.")
        sys.exit(1)
    else:
        print("✅ All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
