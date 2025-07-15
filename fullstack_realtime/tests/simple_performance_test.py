#!/usr/bin/env python3
"""
Simple Performance Test for Omani Therapist AI
==============================================

A basic performance test to validate the <20 seconds latency requirement
and generate essential performance metrics for the technical assessment.

Author: AI Assistant
Created: 2025-01-15
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from api.omani_therapist_ai import OmaniTherapistAI, TimingMetrics
    from api.main import detect_crisis
except ImportError:
    print("❌ Could not import required modules. Make sure you're running from the project root.")
    sys.exit(1)

class SimplePerformanceTest:
    """Simple performance testing for Omani Therapist AI"""
    
    def __init__(self):
        """Initialize test suite"""
        self.ai_system = None
        
        # Test scenarios
        self.test_inputs = [
            "أحتاج مساعدة في التعامل مع القلق",
            "أشعر بالحزن والاكتئاب مؤخراً", 
            "لدي مشاكل في العلاقات الأسرية",
            "I'm feeling anxious and need help",
            "I have trouble sleeping and feel stressed"
        ]
        
        # Crisis scenarios
        self.crisis_inputs = [
            "أريد أن أموت، لا أستطيع المتابعة",
            "I can't take it anymore, I want to end it all"
        ]
    
    def initialize_system(self) -> bool:
        """Initialize the AI system"""
        try:
            print("🔧 Initializing Omani Therapist AI...")
            self.ai_system = OmaniTherapistAI()
            print("✅ AI system initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize AI system: {e}")
            return False
    
    def test_text_response_latency(self, text: str) -> Dict[str, Any]:
        """Test latency for text-based AI response"""
        print(f"📝 Testing: {text[:50]}...")
        
        start_time = time.time()
        
        try:
            # Create basic timing metrics
            now = time.time()
            timing = TimingMetrics(
                speech_start_time=now,
                speech_end_time=now,
                ai_processing_start_time=now,
                ai_processing_end_time=now,
                tts_start_time=now,
                tts_end_time=now,
                voice_playback_start_time=now
            )
            
            # Get AI response
            if self.ai_system:
                result = self.ai_system.get_ai_response(text, timing)
            else:
                result = None
            
            end_time = time.time()
            latency = end_time - start_time
            
            if result:
                ai_response, detected_language = result
                success = ai_response is not None
            else:
                ai_response = None
                detected_language = 'unknown'
                success = False
            
            test_result = {
                'input_text': text,
                'ai_response': ai_response[:100] + "..." if ai_response and len(ai_response) > 100 else ai_response,
                'detected_language': detected_language,
                'latency_seconds': latency,
                'meets_20s_requirement': latency < 20.0,
                'success': success,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"   ⏱️ Latency: {latency:.2f}s")
            print(f"   ✅ <20s: {test_result['meets_20s_requirement']}")
            print(f"   🎯 Success: {success}")
            
            return test_result
            
        except Exception as e:
            end_time = time.time()
            latency = end_time - start_time
            
            print(f"   ❌ Error: {e}")
            
            return {
                'input_text': text,
                'ai_response': None,
                'detected_language': 'unknown',
                'latency_seconds': latency,
                'meets_20s_requirement': False,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def test_crisis_detection(self) -> List[Dict[str, Any]]:
        """Test crisis detection performance"""
        print("🚨 Testing crisis detection...")
        
        results = []
        
        for crisis_text in self.crisis_inputs:
            start_time = time.time()
            is_crisis = detect_crisis(crisis_text)
            end_time = time.time()
            
            detection_time = end_time - start_time
            
            result = {
                'input_text': crisis_text,
                'is_crisis_detected': is_crisis,
                'detection_time_ms': detection_time * 1000,
                'expected_crisis': True,
                'correct_detection': is_crisis,
                'timestamp': datetime.now().isoformat()
            }
            
            results.append(result)
            print(f"   📝 {crisis_text[:30]}... → Crisis: {is_crisis} ({detection_time*1000:.1f}ms)")
        
        return results
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run all performance tests"""
        print("🚀 Starting Simple Performance Test")
        print("=" * 60)
        
        if not self.initialize_system():
            return {'error': 'Failed to initialize AI system'}
        
        # Test 1: Text Response Latency
        print("\n📝 TEST 1: Text Response Latency")
        print("-" * 40)
        
        text_results = []
        for text in self.test_inputs:
            result = self.test_text_response_latency(text)
            text_results.append(result)
        
        # Test 2: Crisis Detection
        print("\n🚨 TEST 2: Crisis Detection Performance")
        print("-" * 40)
        
        crisis_results = self.test_crisis_detection()
        
        # Calculate statistics
        successful_tests = [r for r in text_results if r['success']]
        latencies = [r['latency_seconds'] for r in successful_tests]
        under_20s_count = sum(1 for r in successful_tests if r['meets_20s_requirement'])
        
        crisis_detection_rate = sum(1 for r in crisis_results if r['correct_detection']) / len(crisis_results) * 100
        avg_crisis_detection_time = sum(r['detection_time_ms'] for r in crisis_results) / len(crisis_results)
        
        # Generate report
        report = {
            'test_metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_tests': len(text_results),
                'crisis_tests': len(crisis_results)
            },
            'performance_summary': {
                'successful_responses': len(successful_tests),
                'success_rate_percent': len(successful_tests) / len(text_results) * 100,
                'average_latency_seconds': sum(latencies) / len(latencies) if latencies else 0,
                'max_latency_seconds': max(latencies) if latencies else 0,
                'min_latency_seconds': min(latencies) if latencies else 0,
                'under_20s_count': under_20s_count,
                'under_20s_rate_percent': under_20s_count / len(successful_tests) * 100 if successful_tests else 0
            },
            'crisis_detection_summary': {
                'detection_rate_percent': crisis_detection_rate,
                'average_detection_time_ms': avg_crisis_detection_time
            },
            'requirements_compliance': {
                'latency_requirement_met': under_20s_count == len(successful_tests) if successful_tests else False,
                'crisis_detection_working': crisis_detection_rate >= 90,
                'system_functional': len(successful_tests) > 0
            },
            'detailed_results': {
                'text_response_tests': text_results,
                'crisis_detection_tests': crisis_results
            }
        }
        
        return report
    
    def save_report(self, report: Dict[str, Any]) -> str:
        """Save test report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"simple_performance_test_report_{timestamp}.json"
        
        # Save in tests directory
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        report_path = os.path.join(tests_dir, filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Report saved: {report_path}")
        return report_path
    
    def print_summary(self, report: Dict[str, Any]):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 SIMPLE PERFORMANCE TEST SUMMARY")
        print("=" * 60)
        
        perf = report['performance_summary']
        crisis = report['crisis_detection_summary']
        compliance = report['requirements_compliance']
        
        print(f"\n🎯 REQUIREMENTS COMPLIANCE:")
        print(f"   ✅ <20s Latency: {compliance['latency_requirement_met']}")
        print(f"   ✅ Crisis Detection: {compliance['crisis_detection_working']}")
        print(f"   ✅ System Functional: {compliance['system_functional']}")
        
        print(f"\n📈 PERFORMANCE METRICS:")
        print(f"   Success Rate: {perf['success_rate_percent']:.1f}%")
        print(f"   Average Latency: {perf['average_latency_seconds']:.2f}s")
        print(f"   Max Latency: {perf['max_latency_seconds']:.2f}s")
        print(f"   Under 20s Rate: {perf['under_20s_rate_percent']:.1f}%")
        
        print(f"\n🚨 CRISIS DETECTION:")
        print(f"   Detection Rate: {crisis['detection_rate_percent']:.1f}%")
        print(f"   Avg Detection Time: {crisis['average_detection_time_ms']:.1f}ms")
        
        print("\n" + "=" * 60)

def main():
    """Main execution function"""
    test = SimplePerformanceTest()
    
    try:
        # Run test
        report = test.run_comprehensive_test()
        
        if 'error' in report:
            print(f"❌ Test failed: {report['error']}")
            return
        
        # Save and display results
        report_path = test.save_report(report)
        test.print_summary(report)
        
        print(f"\n✅ Performance test completed successfully!")
        print(f"📁 Full report: {report_path}")
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 