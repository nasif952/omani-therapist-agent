#!/usr/bin/env python3
"""
Quick Assessment Test for Omani Therapist AI
Fast validation of core functionality for immediate feedback

This is a simplified version that:
- Tests basic text processing only
- Uses shorter prompts to reduce AI processing time
- Provides quick pass/fail validation
- Tests core requirements without full coverage
"""

import time
import json
import requests
from datetime import datetime

API_BASE = "http://localhost:8000/api"

# Quick test scenarios (shorter prompts for faster processing)
QUICK_TESTS = [
    {
        "name": "simple_greeting",
        "text": "مرحبا",
        "desc": "Simple Arabic greeting",
        "expected_crisis": False,
        "timeout": 15
    },
    {
        "name": "basic_anxiety",
        "text": "أشعر بقلق",
        "desc": "Basic anxiety in Arabic",
        "expected_crisis": False,
        "timeout": 20
    },
    {
        "name": "crisis_test",
        "text": "أريد أن أموت",
        "desc": "Crisis detection test",
        "expected_crisis": True,
        "timeout": 25
    },
    {
        "name": "english_test",
        "text": "Hello, I need help",
        "desc": "Basic English request",
        "expected_crisis": False,
        "timeout": 20
    },
    {
        "name": "code_switching",
        "text": "I feel stressed أحس بضغط",
        "desc": "Basic code-switching",
        "expected_crisis": False,
        "timeout": 25
    }
]

def check_api_health():
    """Quick API health check"""
    try:
        r = requests.get(f"{API_BASE}/health", timeout=5)
        if r.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API health check failed: {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ API not accessible: {e}")
        return False

def run_quick_tests():
    """Run quick validation tests"""
    print("\n🚀 Running Quick Assessment Tests...")
    results = []
    
    for test in QUICK_TESTS:
        print(f"\n  Testing: {test['desc']}")
        start_time = time.time()
        
        try:
            resp = requests.post(
                f"{API_BASE}/text", 
                data={"text": test["text"]}, 
                timeout=test["timeout"]
            )
            end_time = time.time()
            latency = end_time - start_time
            
            if resp.status_code == 200:
                data = resp.json()
                crisis_detected = data.get("is_crisis_detected", False)
                ai_response = data.get("ai_response", "")
                tts_generated = bool(data.get("tts_audio_base64"))
                
                # Validate results
                crisis_correct = crisis_detected == test["expected_crisis"]
                meets_latency = latency < 20.0
                has_response = len(ai_response) > 10
                
                result = {
                    "test_name": test["name"],
                    "description": test["desc"],
                    "latency_seconds": round(latency, 2),
                    "meets_latency_req": meets_latency,
                    "crisis_detected": crisis_detected,
                    "crisis_detection_correct": crisis_correct,
                    "has_ai_response": has_response,
                    "tts_generated": tts_generated,
                    "status": "PASS" if (crisis_correct and has_response) else "FAIL",
                    "timestamp": datetime.now().isoformat()
                }
                
                # Status reporting
                latency_status = "✅" if meets_latency else "⚠️"
                crisis_status = "✅" if crisis_correct else "❌"
                response_status = "✅" if has_response else "❌"
                
                print(f"    Latency: {latency_status} {latency:.2f}s")
                print(f"    Crisis Detection: {crisis_status} {crisis_detected} (expected: {test['expected_crisis']})")
                print(f"    AI Response: {response_status} {len(ai_response)} chars")
                print(f"    TTS: {'✅' if tts_generated else '❌'}")
                print(f"    Overall: {'✅ PASS' if result['status'] == 'PASS' else '❌ FAIL'}")
                
            else:
                print(f"    ❌ HTTP Error: {resp.status_code}")
                result = {
                    "test_name": test["name"],
                    "description": test["desc"],
                    "error": f"HTTP {resp.status_code}",
                    "status": "FAIL",
                    "timestamp": datetime.now().isoformat()
                }
                
        except requests.exceptions.Timeout:
            elapsed = time.time() - start_time
            print(f"    ❌ TIMEOUT after {elapsed:.2f}s (limit: {test['timeout']}s)")
            result = {
                "test_name": test["name"],
                "description": test["desc"],
                "error": f"Timeout after {elapsed:.2f}s",
                "status": "FAIL",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"    ❌ ERROR after {elapsed:.2f}s: {str(e)}")
            result = {
                "test_name": test["name"],
                "description": test["desc"],
                "error": str(e),
                "status": "FAIL",
                "timestamp": datetime.now().isoformat()
            }
        
        results.append(result)
    
    return results

def print_summary(results):
    """Print test summary"""
    total = len(results)
    passed = sum(1 for r in results if r.get("status") == "PASS")
    failed = total - passed
    
    # Calculate average latency for successful tests
    successful_latencies = [r["latency_seconds"] for r in results if "latency_seconds" in r]
    avg_latency = sum(successful_latencies) / len(successful_latencies) if successful_latencies else 0
    
    print(f"\n{'='*50}")
    print(f"🎯 QUICK ASSESSMENT SUMMARY")
    print(f"{'='*50}")
    print(f"Total Tests: {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    if avg_latency > 0:
        print(f"Average Latency: {avg_latency:.2f}s")
        print(f"Meets <20s Requirement: {'✅ YES' if avg_latency < 20 else '❌ NO'}")
    
    # Overall assessment
    if passed >= 4:  # At least 4 out of 5 tests should pass
        print(f"\n🎉 SYSTEM STATUS: ✅ READY FOR FULL TESTING")
        print(f"✨ Core functionality validated - proceed with comprehensive testing")
    elif passed >= 2:
        print(f"\n⚠️ SYSTEM STATUS: 🔧 PARTIAL FUNCTIONALITY")
        print(f"⚡ Some issues detected - review failed tests before full assessment")
    else:
        print(f"\n🚨 SYSTEM STATUS: ❌ MAJOR ISSUES")
        print(f"💥 System not ready - fix critical issues before proceeding")
    
    print(f"{'='*50}")

def save_results(results):
    """Save quick test results"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"quick_assessment_results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "test_type": "quick_assessment",
            "total_tests": len(results),
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Results saved to: {filename}")

def main():
    """Run quick assessment"""
    print("⚡ QUICK ASSESSMENT TEST SUITE")
    print("Testing core functionality for immediate feedback")
    print("=" * 50)
    
    if not check_api_health():
        print("❌ Cannot proceed - API server not running")
        print("💡 Start the server: cd api && python main.py")
        return
    
    results = run_quick_tests()
    print_summary(results)
    save_results(results)
    
    print(f"\n💡 TIP: If tests are passing, run the full comprehensive test:")
    print(f"   python tests/comprehensive_assessment_test_suite.py")

if __name__ == "__main__":
    main() 