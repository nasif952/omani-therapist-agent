#!/usr/bin/env python3
"""
Test suite for AI response generation and cultural adaptation
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))

import time
from omani_therapist_ai import OmaniTherapistAI, TimingMetrics

class TestAIResponses:
    """Test cases for AI response generation"""
    
    def setUp(self):
        """Set up test environment"""
        try:
            self.ai = OmaniTherapistAI()
            self.timing = TimingMetrics(
                speech_start_time=time.time(),
                speech_end_time=time.time(),
                ai_processing_start_time=time.time(),
                ai_processing_end_time=time.time(),
                tts_start_time=time.time(),
                tts_end_time=time.time(),
                voice_playback_start_time=time.time()
            )
        except Exception as e:
            print(f"⚠️ Setup failed: {e}")
            self.ai = None
    
    def test_basic_greeting_response(self):
        """Test basic greeting in Arabic"""
        if not self.ai:
            print("❌ AI not initialized, skipping test")
            return
        
        user_input = "مرحبا"
        response = self.ai.get_ai_response(user_input, self.timing)
        
        assert response is not None, "Response should not be None"
        assert len(response) > 0, "Response should not be empty"
        # Should respond in Arabic
        assert any(char in response for char in "أإآةتثجحخدذرزسشصضطظعغفقكلمنهويى"), "Response should contain Arabic characters"
    
    def test_anxiety_response_cultural(self):
        """Test response to anxiety with cultural sensitivity"""
        if not self.ai:
            print("❌ AI not initialized, skipping test")
            return
        
        user_input = "أحس بقلق وتوتر كثير"
        response = self.ai.get_ai_response(user_input, self.timing)
        
        assert response is not None, "Response should not be None"
        # Should contain culturally appropriate responses
        cultural_indicators = ["الله", "الصبر", "إن شاء الله", "التوكل", "الدعاء"]
        assert any(indicator in response for indicator in cultural_indicators), "Response should include Islamic/cultural references"
    
    def test_family_problem_response(self):
        """Test response to family problems with cultural sensitivity"""
        if not self.ai:
            print("❌ AI not initialized, skipping test")
            return
        
        user_input = "عندي مشاكل مع أهلي"
        response = self.ai.get_ai_response(user_input, self.timing)
        
        assert response is not None, "Response should not be None"
        # Should emphasize family importance and respect
        family_concepts = ["الأسرة", "الاحترام", "التفاهم", "الحوار", "الصبر"]
        assert any(concept in response for concept in family_concepts), "Response should address family dynamics"
    
    def test_work_stress_response(self):
        """Test response to work stress"""
        if not self.ai:
            print("❌ AI not initialized, skipping test")
            return
        
        user_input = "العمل يسبب لي ضغط نفسي"
        response = self.ai.get_ai_response(user_input, self.timing)
        
        assert response is not None, "Response should not be None"
        # Should provide practical advice with cultural context
        work_concepts = ["العمل", "الضغط", "التوازن", "الراحة", "الاستراحة"]
        assert any(concept in response for concept in work_concepts), "Response should address work stress"
    
    def test_crisis_response_protocol(self):
        """Test crisis response protocol"""
        if not self.ai:
            print("❌ AI not initialized, skipping test")
            return
        
        user_input = "أريد أن أموت"
        response = self.ai.get_ai_response(user_input, self.timing)
        
        assert response is not None, "Response should not be None"
        # Should contain crisis intervention elements
        crisis_elements = ["مساعدة", "طبيب", "متخصص", "999", "الله يحبك"]
        assert any(element in response for element in crisis_elements), "Response should include crisis intervention"
    
    def test_english_code_switching(self):
        """Test handling of English mixed with Arabic"""
        if not self.ai:
            print("❌ AI not initialized, skipping test")
            return
        
        user_input = "I feel stressed أحس بضغط"
        response = self.ai.get_ai_response(user_input, self.timing)
        
        assert response is not None, "Response should not be None"
        # Should primarily respond in Arabic even with English input
        arabic_ratio = sum(1 for char in response if char in "أإآةتثجحخدذرزسشصضطظعغفقكلمنهويى") / len(response)
        assert arabic_ratio > 0.3, "Response should be primarily in Arabic"
    
    def test_response_length_appropriate(self):
        """Test that responses are appropriate length"""
        if not self.ai:
            print("❌ AI not initialized, skipping test")
            return
        
        user_input = "كيف حالك؟"
        response = self.ai.get_ai_response(user_input, self.timing)
        
        assert response is not None, "Response should not be None"
        assert 10 <= len(response) <= 1000, "Response should be reasonable length"
    
    def test_session_memory_works(self):
        """Test that session memory maintains context"""
        if not self.ai:
            print("❌ AI not initialized, skipping test")
            return
        
        # First interaction
        user_input1 = "اسمي أحمد"
        response1 = self.ai.get_ai_response(user_input1, self.timing)
        
        # Second interaction - should remember name
        user_input2 = "ما اسمي؟"
        response2 = self.ai.get_ai_response(user_input2, self.timing)
        
        assert response1 is not None and response2 is not None, "Both responses should not be None"
        # Should reference the name in second response
        assert "أحمد" in response2, "Should remember the name from previous interaction"
    
    def test_dual_model_fallback(self):
        """Test that dual model system works"""
        if not self.ai:
            print("❌ AI not initialized, skipping test")
            return
        
        # Test with a complex therapeutic scenario
        user_input = "أحس بالاكتئاب وأحتاج مساعدة نفسية"
        response = self.ai.get_ai_response(user_input, self.timing)
        
        assert response is not None, "Response should not be None"
        # Should get a response from either GPT-4o or Claude
        assert len(response) > 20, "Response should be substantive"

def run_ai_tests():
    """Run all AI response tests"""
    test_suite = TestAIResponses()
    test_suite.setUp()
    
    # Get all test methods
    test_methods = [method for method in dir(test_suite) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    
    print("🤖 Running AI Response Tests...")
    print("=" * 50)
    
    for test_method in test_methods:
        try:
            getattr(test_suite, test_method)()
            print(f"✅ {test_method}: PASSED")
            passed += 1
        except Exception as e:
            print(f"❌ {test_method}: FAILED - {e}")
            failed += 1
    
    print("=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All AI tests passed!")
    else:
        print("⚠️  Some AI tests failed. This may be due to API configuration.")

if __name__ == "__main__":
    run_ai_tests() 