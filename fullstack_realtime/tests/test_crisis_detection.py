#!/usr/bin/env python3
"""
Test suite for crisis detection functionality
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))

import pytest
from main import detect_crisis, enhance_ai_prompt_for_crisis

class TestCrisisDetection:
    """Test cases for crisis detection system"""
    
    def test_suicide_keywords_english(self):
        """Test detection of suicide-related keywords in English"""
        crisis_texts = [
            "I want to kill myself",
            "I'm thinking about suicide",
            "I want to end my life",
            "I can't take it anymore, I want to die"
        ]
        
        for text in crisis_texts:
            assert detect_crisis(text) == True, f"Failed to detect crisis in: {text}"
    
    def test_suicide_keywords_arabic(self):
        """Test detection of suicide-related keywords in Arabic"""
        crisis_texts = [
            "أريد أن أموت",
            "أفكر في الانتحار",
            "اقتل نفسي",
            "أنهي حياتي",
            "أبي أموت"
        ]
        
        for text in crisis_texts:
            assert detect_crisis(text) == True, f"Failed to detect crisis in: {text}"
    
    def test_self_harm_keywords(self):
        """Test detection of self-harm keywords"""
        crisis_texts = [
            "I want to hurt myself",
            "أؤذي نفسي",
            "أجرح نفسي",
            "I'm going to cut myself",
            "أعذب نفسي"
        ]
        
        for text in crisis_texts:
            assert detect_crisis(text) == True, f"Failed to detect crisis in: {text}"
    
    def test_hopelessness_keywords(self):
        """Test detection of hopelessness expressions"""
        crisis_texts = [
            "I give up, there's no hope",
            "مافي أمل",
            "تعبت من الحياة",
            "I can't go on",
            "ما عاد أقدر"
        ]
        
        for text in crisis_texts:
            assert detect_crisis(text) == True, f"Failed to detect crisis in: {text}"
    
    def test_omani_dialect_crisis(self):
        """Test detection of crisis expressions in Omani dialect"""
        crisis_texts = [
            "أبي أخلص",
            "خلاص تعبت",
            "مافي فايدة مني",
            "أحس أني عبء",
            "الناس أحسن بدوني"
        ]
        
        for text in crisis_texts:
            assert detect_crisis(text) == True, f"Failed to detect crisis in: {text}"
    
    def test_mental_health_crisis(self):
        """Test detection of mental health crisis terms"""
        crisis_texts = [
            "I'm having a mental breakdown",
            "انهيار نفسي",
            "I'm losing my mind",
            "أفقد عقلي",
            "أحس أني أجن"
        ]
        
        for text in crisis_texts:
            assert detect_crisis(text) == True, f"Failed to detect crisis in: {text}"
    
    def test_help_requests(self):
        """Test detection of urgent help requests"""
        crisis_texts = [
            "Help me please",
            "ساعدني",
            "أحتاج مساعدة عاجلة",
            "Save me",
            "أنقذني"
        ]
        
        for text in crisis_texts:
            assert detect_crisis(text) == True, f"Failed to detect crisis in: {text}"
    
    def test_non_crisis_text(self):
        """Test that normal text doesn't trigger crisis detection"""
        normal_texts = [
            "Hello, how are you?",
            "مرحبا، كيف حالك؟",
            "I'm feeling a bit sad today",
            "أحس بحزن اليوم",
            "Work is stressful",
            "العمل متعب",
            "I need help with my homework",
            "أحتاج مساعدة في الواجب"
        ]
        
        for text in normal_texts:
            assert detect_crisis(text) == False, f"False positive for: {text}"
    
    def test_crisis_prompt_enhancement(self):
        """Test that crisis prompt enhancement works correctly"""
        user_text = "I want to kill myself"
        enhanced_prompt = enhance_ai_prompt_for_crisis(user_text, True)
        
        # Check that crisis guidance is added
        assert "CRITICAL CRISIS RESPONSE PROTOCOL" in enhanced_prompt
        assert "Emergency: 999" in enhanced_prompt
        assert "رحمة الله واسعة" in enhanced_prompt
        assert user_text in enhanced_prompt
    
    def test_non_crisis_prompt_enhancement(self):
        """Test that non-crisis text passes through unchanged"""
        user_text = "I'm feeling a bit stressed"
        enhanced_prompt = enhance_ai_prompt_for_crisis(user_text, False)
        
        # Should return original text
        assert enhanced_prompt == user_text
    
    def test_case_insensitive_detection(self):
        """Test that crisis detection works regardless of case"""
        crisis_texts = [
            "I WANT TO KILL MYSELF",
            "help me please",
            "SUICIDE",
            "انتحار"
        ]
        
        for text in crisis_texts:
            assert detect_crisis(text) == True, f"Failed case-insensitive detection for: {text}"
    
    def test_mixed_language_crisis(self):
        """Test detection in mixed Arabic-English text"""
        crisis_texts = [
            "I feel like أريد أن أموت",
            "Help me ساعدني please",
            "انتحار is what I'm thinking about"
        ]
        
        for text in crisis_texts:
            assert detect_crisis(text) == True, f"Failed mixed language detection for: {text}"

if __name__ == "__main__":
    # Run tests
    test_suite = TestCrisisDetection()
    
    # Get all test methods
    test_methods = [method for method in dir(test_suite) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    
    print("🧪 Running Crisis Detection Tests...")
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
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Please review the crisis detection logic.") 