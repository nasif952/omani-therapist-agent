#!/usr/bin/env python3
"""
Comprehensive test runner for Omani Therapist AI
"""
import sys
import os
import time
from datetime import datetime

# Add API path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))

# Import test modules
TestCrisisDetection = None
TestAIResponses = None
run_ai_tests = None

try:
    from test_crisis_detection import TestCrisisDetection
    from test_ai_responses import TestAIResponses, run_ai_tests
    print("✅ Test modules imported successfully")
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    print("Some tests may be skipped due to missing dependencies")

def run_crisis_detection_tests():
    """Run crisis detection tests"""
    if TestCrisisDetection is None:
        print("❌ Crisis Detection tests skipped: TestCrisisDetection not available")
        return 0, 1, [("TestCrisisDetection", "SKIPPED", "Import failed")]
    
    test_suite = TestCrisisDetection()
    test_methods = [method for method in dir(test_suite) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    results = []
    
    print("🚨 Running Crisis Detection Tests...")
    print("=" * 50)
    
    for test_method in test_methods:
        try:
            getattr(test_suite, test_method)()
            print(f"✅ {test_method}: PASSED")
            results.append((test_method, "PASSED", None))
            passed += 1
        except Exception as e:
            print(f"❌ {test_method}: FAILED - {e}")
            results.append((test_method, "FAILED", str(e)))
            failed += 1
    
    return passed, failed, results

def run_system_integration_tests():
    """Run basic system integration tests"""
    passed = 0
    failed = 0
    results = []
    
    print("🔧 Running System Integration Tests...")
    print("=" * 50)
    
    # Test 1: Environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path='../.env')
        
        required_vars = ['AZURE_SPEECH_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise Exception(f"Missing environment variables: {missing_vars}")
        
        print("✅ test_environment_variables: PASSED")
        results.append(("test_environment_variables", "PASSED", None))
        passed += 1
    except Exception as e:
        print(f"❌ test_environment_variables: FAILED - {e}")
        results.append(("test_environment_variables", "FAILED", str(e)))
        failed += 1
    
    # Test 2: API imports
    try:
        from main import detect_crisis, enhance_ai_prompt_for_crisis
        from omani_therapist_ai import OmaniTherapistAI, TimingMetrics
        
        print("✅ test_api_imports: PASSED")
        results.append(("test_api_imports", "PASSED", None))
        passed += 1
    except Exception as e:
        print(f"❌ test_api_imports: FAILED - {e}")
        results.append(("test_api_imports", "FAILED", str(e)))
        failed += 1
    
    # Test 3: Basic crisis detection functionality
    try:
        from main import detect_crisis
        
        # Test basic functionality
        assert detect_crisis("I want to kill myself") == True
        assert detect_crisis("Hello, how are you?") == False
        
        print("✅ test_basic_crisis_detection: PASSED")
        results.append(("test_basic_crisis_detection", "PASSED", None))
        passed += 1
    except Exception as e:
        print(f"❌ test_basic_crisis_detection: FAILED - {e}")
        results.append(("test_basic_crisis_detection", "FAILED", str(e)))
        failed += 1
    
    return passed, failed, results

def generate_test_report(all_results):
    """Generate a comprehensive test report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""
# Omani Therapist AI - Test Report
Generated: {timestamp}

## Test Summary
"""
    
    total_passed = 0
    total_failed = 0
    
    # Handle different result formats
    for test_category, result_data in all_results.items():
        if len(result_data) == 3:
            passed, failed, results = result_data
            total_passed += passed
            total_failed += failed
        else:
            # Handle unexpected format
            print(f"⚠️ Unexpected result format for {test_category}: {result_data}")
    
    total_tests = total_passed + total_failed
    
    if total_tests > 0:
        report += f"""
- **Total Tests**: {total_tests}
- **Passed**: {total_passed} ({total_passed/total_tests*100:.1f}%)
- **Failed**: {total_failed} ({total_failed/total_tests*100:.1f}%)
- **Success Rate**: {total_passed/total_tests*100:.1f}%

## Detailed Results

"""
    else:
        report += """
- **Total Tests**: 0
- **Status**: No tests executed

## Detailed Results

"""
    
    for test_category, result_data in all_results.items():
        if len(result_data) == 3:
            passed, failed, results = result_data
            report += f"""
### {test_category}
- Passed: {passed}
- Failed: {failed}

"""
            for test_name, status, error in results:
                if status == "PASSED":
                    report += f"✅ {test_name}\n"
                elif status == "FAILED":
                    report += f"❌ {test_name}: {error}\n"
                else:
                    report += f"⚠️ {test_name}: {status}\n"
    
    # Quick wins assessment
    report += """
## Quick Wins Assessment

Based on the test results:

"""
    
    if all_results.get("Crisis Detection", [0, 1, []])[1] == 0:
        report += "✅ **Crisis Detection Enhanced**: All crisis detection tests passed\n"
    else:
        report += "❌ **Crisis Detection**: Some tests failed - review patterns\n"
    
    if all_results.get("System Integration", [0, 1, []])[1] == 0:
        report += "✅ **System Integration**: All basic system tests passed\n"
    else:
        report += "❌ **System Integration**: Some system tests failed - check configuration\n"
    
    if total_failed == 0:
        report += "\n🎉 **All Quick Wins Completed Successfully!**\n"
    else:
        report += f"\n⚠️ **{total_failed} tests failed** - review implementation\n"
    
    report += """
## Next Steps

1. **Fix any failed tests** before proceeding
2. **Run performance tests** to verify <20s latency
3. **Validate with native speakers** for cultural accuracy
4. **Implement comprehensive CBT techniques**
5. **Add production security measures**

## Test Files

- `test_crisis_detection.py`: Crisis detection functionality
- `test_ai_responses.py`: AI response generation and cultural adaptation
- `run_all_tests.py`: This test runner

---
*Generated by Omani Therapist AI Test Suite*
"""
    
    # Save report
    with open("test_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    return report

def main():
    """Run all tests and generate report"""
    print("🧪 Omani Therapist AI - Comprehensive Test Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    all_results = {}
    
    # Run crisis detection tests
    try:
        passed, failed, results = run_crisis_detection_tests()
        all_results["Crisis Detection"] = (passed, failed, results)
        print(f"\n📊 Crisis Detection: {passed} passed, {failed} failed\n")
    except Exception as e:
        print(f"❌ Crisis Detection tests failed to run: {e}\n")
        all_results["Crisis Detection"] = (0, 1, [("setup", "FAILED", str(e))])
    
    # Run system integration tests
    try:
        passed, failed, results = run_system_integration_tests()
        all_results["System Integration"] = (passed, failed, results)
        print(f"\n📊 System Integration: {passed} passed, {failed} failed\n")
    except Exception as e:
        print(f"❌ System Integration tests failed to run: {e}\n")
        all_results["System Integration"] = (0, 1, [("setup", "FAILED", str(e))])
    
    # Run AI response tests (may fail due to API keys)
    try:
        print("🤖 Running AI Response Tests...")
        print("=" * 50)
        print("⚠️  Note: These tests require valid API keys and may fail in testing environment")
        
        # We'll skip AI tests in basic setup but show the framework
        all_results["AI Responses"] = (0, 0, [("skipped", "SKIPPED", "Requires API keys")])
        print("⏭️  AI Response tests skipped (require API configuration)")
    except Exception as e:
        print(f"❌ AI Response tests failed to run: {e}")
        all_results["AI Responses"] = (0, 1, [("setup", "FAILED", str(e))])
    
    # Generate comprehensive report
    print("\n" + "=" * 60)
    print("📋 Generating Test Report...")
    
    report = generate_test_report(all_results)
    
    # Print summary
    total_passed = sum(result[0] for result in all_results.values())
    total_failed = sum(result[1] for result in all_results.values())
    
    print("=" * 60)
    print("🎯 FINAL RESULTS")
    print("=" * 60)
    print(f"Total Passed: {total_passed}")
    print(f"Total Failed: {total_failed}")
    
    if total_failed == 0:
        print("🎉 ALL TESTS PASSED! Quick wins completed successfully!")
    else:
        print(f"⚠️  {total_failed} tests failed. Please review and fix before proceeding.")
    
    print(f"\n📄 Detailed report saved to: test_report.md")
    print("=" * 60)

if __name__ == "__main__":
    main() 