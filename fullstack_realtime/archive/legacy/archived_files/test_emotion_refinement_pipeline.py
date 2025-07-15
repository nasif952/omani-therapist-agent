#!/usr/bin/env python3
"""
Advanced Emotion Refinement Pipeline Test
==========================================

Test script to demonstrate the two-stage emotion refinement system:
Stage 1: Basic AI response generation
Stage 2: GPT-4.1-mini emotion refinement with natural expressions

This test compares:
- Basic emotion detection vs GPT-4.1-mini refinement
- Original responses vs emotionally enhanced responses
- Different emotional scenarios and crisis levels
- Arabic vs English responses
- Performance metrics and enhancement statistics

Author: AI Assistant
Created: 2024
"""

import os
import sys
import asyncio
import time
from typing import List, Dict, Any
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from omani_therapist_ai import OmaniTherapistAI, TimingMetrics
from emotion_refiner import EmotionRefiner, EmotionContext, RefinedResponse

class EmotionRefinementTester:
    """Comprehensive tester for the emotion refinement pipeline"""
    
    def __init__(self):
        """Initialize the tester with AI system"""
        print("🚀 Initializing Advanced Emotion Refinement Test System...")
        self.ai = OmaniTherapistAI()
        self.test_results = []
        
    def create_test_scenarios(self) -> List[Dict[str, Any]]:
        """Create comprehensive test scenarios for different emotional contexts"""
        return [
            {
                'name': 'Anxious Student - Arabic',
                'user_input': 'أشعر بقلق شديد من الامتحانات وأخاف من الفشل',
                'language': 'ar',
                'expected_emotions': ['calm', 'encouraging'],
                'crisis_level': 'mild',
                'description': 'Student anxiety about exams - should receive calming, encouraging response'
            },
            {
                'name': 'Excited Achievement - English',
                'user_input': 'I finally got the promotion I\'ve been working towards! I\'m so happy!',
                'language': 'en',
                'expected_emotions': ['excited', 'encouraging'],
                'crisis_level': 'none',
                'description': 'Celebrating achievement - should receive enthusiastic, celebratory response'
            },
            {
                'name': 'Deep Sadness - Arabic',
                'user_input': 'فقدت والدي مؤخراً وأشعر بحزن عميق ولا أعرف كيف أتعامل مع هذا',
                'language': 'ar',
                'expected_emotions': ['sad', 'empathy'],
                'crisis_level': 'moderate',
                'description': 'Grief counseling - should receive empathetic, supportive response with Islamic comfort'
            },
            {
                'name': 'Relationship Issues - English',
                'user_input': 'My relationship is falling apart and I don\'t know what to do. I feel lost.',
                'language': 'en',
                'expected_emotions': ['empathy', 'calm'],
                'crisis_level': 'mild',
                'description': 'Relationship problems - should receive empathetic guidance'
            },
            {
                'name': 'Work Stress - Arabic',
                'user_input': 'ضغط العمل يقتلني، مديري يطلب المستحيل ولا أستطيع التعامل مع هذا',
                'language': 'ar',
                'expected_emotions': ['empathy', 'calm'],
                'crisis_level': 'moderate',
                'description': 'Work burnout - should receive stress management guidance'
            },
            {
                'name': 'Breakthrough Moment - English',
                'user_input': 'I just realized something about myself through our conversations. I think I understand my patterns now!',
                'language': 'en',
                'expected_emotions': ['excited', 'encouraging'],
                'crisis_level': 'none',
                'description': 'Therapeutic breakthrough - should receive validation and enthusiasm'
            }
        ]
    
    async def run_single_test(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test scenario and compare basic vs refined responses"""
        print(f"\n{'='*60}")
        print(f"🧪 Testing: {scenario['name']}")
        print(f"📝 Description: {scenario['description']}")
        print(f"👤 User Input: {scenario['user_input']}")
        print(f"🌍 Language: {scenario['language']}")
        print(f"⚠️  Expected Crisis Level: {scenario['crisis_level']}")
        
        # Create timing metrics
        timing = TimingMetrics(
            speech_start_time=time.time(),
            speech_end_time=time.time(),
            ai_processing_start_time=time.time(),
            ai_processing_end_time=time.time(),
            tts_start_time=time.time(),
            tts_end_time=time.time(),
            voice_playback_start_time=time.time()
        )
        
        # Stage 1: Get basic AI response
        print(f"\n🤖 Stage 1: Basic AI Response Generation...")
        start_time = time.time()
        result = self.ai.get_ai_response(scenario['user_input'], timing)
        stage1_time = time.time() - start_time
        
        if not result or not result[0]:
            print("❌ Failed to get AI response")
            return {'status': 'failed', 'error': 'No AI response'}
        
        original_response, detected_language = result
        if not original_response:
            print("❌ Empty AI response")
            return {'status': 'failed', 'error': 'Empty AI response'}
            
        print(f"✅ Original Response: {original_response[:100]}...")
        print(f"🔍 Detected Language: {detected_language}")
        
        # Basic emotion detection
        basic_emotion = self.ai.detect_emotion_from_text(original_response)
        print(f"📊 Basic Emotion Detected: {basic_emotion}")
        
        # Stage 2: Advanced emotion refinement
        print(f"\n✨ Stage 2: GPT-4.1-mini Emotion Refinement...")
        
        if self.ai.use_emotion_refinement:
            start_time = time.time()
            refined_response, enhanced_ssml = self.ai.refine_ai_response_with_emotion(
                original_response, scenario['user_input'], detected_language
            )
            stage2_time = time.time() - start_time
            
            print(f"🎭 Refined Response: {refined_response}")
            print(f"⏱️  Refinement Time: {stage2_time:.2f}s")
            
            # Analyze refinement quality
            refinement_analysis = self._analyze_refinement_quality(original_response, refined_response)
            print(f"📈 Refinement Analysis: {refinement_analysis}")
            
        else:
            print("⚠️  Emotion refinement disabled - using basic response")
            refined_response = original_response
            enhanced_ssml = ""
            stage2_time = 0
            refinement_analysis = {'enhancement_count': 0, 'natural_expressions': 0}
        
        # Compare responses
        comparison = self._compare_responses(original_response, refined_response, scenario['expected_emotions'])
        
        # Test results
        test_result = {
            'scenario': scenario['name'],
            'user_input': scenario['user_input'],
            'language': detected_language,
            'crisis_level': scenario['crisis_level'],
            'stage1_time': stage1_time,
            'stage2_time': stage2_time,
            'total_time': stage1_time + stage2_time,
            'original_response': original_response,
            'refined_response': refined_response,
            'basic_emotion': basic_emotion,
            'expected_emotions': scenario['expected_emotions'],
            'refinement_used': self.ai.use_emotion_refinement,
            'refinement_analysis': refinement_analysis,
            'comparison': comparison,
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_results.append(test_result)
        
        print(f"\n📊 Test Summary:")
        print(f"   ⏱️  Total Processing Time: {test_result['total_time']:.2f}s")
        print(f"   🎯 Emotion Match: {comparison['emotion_match']}")
        print(f"   ✨ Enhancement Quality: {comparison['enhancement_score']}/10")
        
        return test_result
    
    def _analyze_refinement_quality(self, original: str, refined: str) -> Dict[str, Any]:
        """Analyze the quality of emotion refinement"""
        # Count emotional expressions added
        natural_expressions = [
            '*sigh*', '*تنهد*', '*pause*', '*وقفة*', 'um...', 'أه...', '...', '____',
            'well...', 'يعني...', '*soft sigh*', '*تنهد خفيف*', '*brief pause*', '*وقفة قصيرة*'
        ]
        
        enhancement_count = 0
        natural_expr_count = 0
        
        for expr in natural_expressions:
            if expr in refined and expr not in original:
                if any(x in expr for x in ['*', '...', '____']):
                    natural_expr_count += 1
                enhancement_count += 1
        
        # Calculate improvement metrics
        length_increase = len(refined) - len(original)
        relative_improvement = length_increase / len(original) if len(original) > 0 else 0
        
        return {
            'enhancement_count': enhancement_count,
            'natural_expressions': natural_expr_count,
            'length_increase': length_increase,
            'relative_improvement': relative_improvement,
            'has_emotional_markers': any(marker in refined for marker in ['*', '...', 'أه', 'um']),
            'estimated_quality': min(10, enhancement_count * 2 + natural_expr_count)
        }
    
    def _compare_responses(self, original: str, refined: str, expected_emotions: List[str]) -> Dict[str, Any]:
        """Compare original vs refined responses"""
        
        # Check if expected emotions are present
        emotion_keywords = {
            'calm': ['calm', 'relax', 'breathe', 'هدوء', 'استرخي', 'تنفس'],
            'encouraging': ['you can', 'strong', 'تستطيع', 'قوي', 'ممتاز'],
            'excited': ['wonderful', 'amazing', 'رائع', 'مبروك', 'excellent'],
            'sad': ['sorry', 'difficult', 'understand', 'أسف', 'صعب', 'أفهم'],
            'empathy': ['hear you', 'feel for', 'أحس بيك', 'معك', 'أتفهم']
        }
        
        original_emotion_match = 0
        refined_emotion_match = 0
        
        for emotion in expected_emotions:
            if emotion in emotion_keywords:
                original_keywords = sum(1 for keyword in emotion_keywords[emotion] if keyword.lower() in original.lower())
                refined_keywords = sum(1 for keyword in emotion_keywords[emotion] if keyword.lower() in refined.lower())
                
                if original_keywords > 0:
                    original_emotion_match += 1
                if refined_keywords > 0:
                    refined_emotion_match += 1
        
        # Calculate enhancement score
        enhancement_score = 0
        if refined != original:
            if refined_emotion_match >= original_emotion_match:
                enhancement_score += 3
            if any(marker in refined for marker in ['*', '...', 'أه', 'um']):
                enhancement_score += 3
            if len(refined) > len(original):
                enhancement_score += 2
            if refined_emotion_match > original_emotion_match:
                enhancement_score += 2
        
        return {
            'emotion_match': refined_emotion_match >= len(expected_emotions) // 2,
            'original_emotion_score': original_emotion_match,
            'refined_emotion_score': refined_emotion_match,
            'enhancement_score': min(10, enhancement_score),
            'is_improved': refined_emotion_match > original_emotion_match or any(marker in refined for marker in ['*', '...'])
        }
    
    async def run_comprehensive_test(self):
        """Run the complete test suite"""
        print("🌟 Starting Comprehensive Emotion Refinement Pipeline Test")
        print("=" * 70)
        
        # Check if emotion refinement is available
        if self.ai.use_emotion_refinement:
            print("✅ GPT-4.1-mini Emotion Refinement: ENABLED")
        else:
            print("⚠️  GPT-4.1-mini Emotion Refinement: DISABLED (using basic detection)")
        
        scenarios = self.create_test_scenarios()
        print(f"📋 Running {len(scenarios)} test scenarios...")
        
        # Run all tests
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{'🧪 Test ' + str(i)}")
            await self.run_single_test(scenario)
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(1)
        
        # Generate comprehensive report
        self.generate_final_report()
    
    def generate_final_report(self):
        """Generate comprehensive test results report"""
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE TEST RESULTS REPORT")
        print("=" * 70)
        
        if not self.test_results:
            print("❌ No test results available")
            return
        
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if 'error' not in r])
        refinement_used = len([r for r in self.test_results if r.get('refinement_used', False)])
        
        # Performance metrics
        avg_stage1_time = sum(r.get('stage1_time', 0) for r in self.test_results) / total_tests
        avg_stage2_time = sum(r.get('stage2_time', 0) for r in self.test_results) / total_tests
        avg_total_time = sum(r.get('total_time', 0) for r in self.test_results) / total_tests
        
        # Quality metrics
        emotion_matches = len([r for r in self.test_results if r.get('comparison', {}).get('emotion_match', False)])
        avg_enhancement_score = sum(r.get('comparison', {}).get('enhancement_score', 0) for r in self.test_results) / total_tests
        improved_responses = len([r for r in self.test_results if r.get('comparison', {}).get('is_improved', False)])
        
        print(f"📈 PERFORMANCE SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")
        print(f"   Refinement Used: {refinement_used}/{total_tests} ({refinement_used/total_tests*100:.1f}%)")
        
        print(f"\n⏱️  TIMING ANALYSIS:")
        print(f"   Average Stage 1 (Basic AI): {avg_stage1_time:.2f}s")
        print(f"   Average Stage 2 (Refinement): {avg_stage2_time:.2f}s")
        print(f"   Average Total Time: {avg_total_time:.2f}s")
        print(f"   Refinement Overhead: {avg_stage2_time/avg_stage1_time*100:.1f}% of base time")
        
        print(f"\n🎯 QUALITY ANALYSIS:")
        print(f"   Emotion Matches: {emotion_matches}/{total_tests} ({emotion_matches/total_tests*100:.1f}%)")
        print(f"   Average Enhancement Score: {avg_enhancement_score:.1f}/10")
        print(f"   Improved Responses: {improved_responses}/{total_tests} ({improved_responses/total_tests*100:.1f}%)")
        
        # Language breakdown
        arabic_tests = len([r for r in self.test_results if r.get('language') == 'ar'])
        english_tests = len([r for r in self.test_results if r.get('language') == 'en'])
        
        print(f"\n🌍 LANGUAGE BREAKDOWN:")
        print(f"   Arabic Tests: {arabic_tests}")
        print(f"   English Tests: {english_tests}")
        
        # Crisis level breakdown
        crisis_levels = {}
        for result in self.test_results:
            level = result.get('crisis_level', 'unknown')
            crisis_levels[level] = crisis_levels.get(level, 0) + 1
        
        print(f"\n⚠️  CRISIS LEVEL DISTRIBUTION:")
        for level, count in crisis_levels.items():
            print(f"   {level.title()}: {count}")
        
        # Best and worst performing scenarios
        if self.test_results:
            best_test = max(self.test_results, key=lambda x: x.get('comparison', {}).get('enhancement_score', 0))
            worst_test = min(self.test_results, key=lambda x: x.get('comparison', {}).get('enhancement_score', 0))
            
            print(f"\n🏆 BEST PERFORMING SCENARIO:")
            print(f"   {best_test['scenario']} (Score: {best_test.get('comparison', {}).get('enhancement_score', 0)}/10)")
            
            print(f"\n⚠️  NEEDS IMPROVEMENT:")
            print(f"   {worst_test['scenario']} (Score: {worst_test.get('comparison', {}).get('enhancement_score', 0)}/10)")
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"emotion_refinement_test_results_{timestamp}.json"
        
        try:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2, ensure_ascii=False, default=str)
            print(f"\n💾 Detailed results saved to: {results_file}")
        except Exception as e:
            print(f"\n❌ Failed to save results: {e}")
        
        print("\n" + "=" * 70)
        if refinement_used > 0:
            print("🎉 Advanced Emotion Refinement Pipeline Test Complete!")
            if avg_enhancement_score > 6:
                print("✨ Emotion refinement system is performing excellently!")
            elif avg_enhancement_score > 4:
                print("👍 Emotion refinement system is performing well.")
            else:
                print("⚠️  Emotion refinement system needs optimization.")
        else:
            print("📝 Basic emotion detection system tested successfully.")
        print("=" * 70)

async def main():
    """Main test function"""
    try:
        tester = EmotionRefinementTester()
        await tester.run_comprehensive_test()
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 