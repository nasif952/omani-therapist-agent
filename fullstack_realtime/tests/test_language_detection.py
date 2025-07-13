#!/usr/bin/env python3
"""
Test script for language detection functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))

from omani_therapist_ai import OmaniTherapistAI

def test_language_detection():
    """Test language detection functionality"""
    print("Testing Language Detection System")
    print("=" * 50)
    
    # Initialize the AI system
    try:
        therapist_ai = OmaniTherapistAI()
        print("✅ AI system initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize AI system: {e}")
        return False
    
    # Test cases
    test_cases = [
        # English test cases
        ("Hello, how are you today?", "en"),
        ("I am feeling sad and depressed", "en"),
        ("Can you help me with my anxiety?", "en"),
        ("I need someone to talk to", "en"),
        
        # Arabic test cases
        ("مرحبا، كيف حالك اليوم؟", "ar"),
        ("أشعر بالحزن والاكتئاب", "ar"),
        ("هل يمكنك مساعدتي مع القلق؟", "ar"),
        ("أحتاج إلى شخص للتحدث معه", "ar"),
        
        # Mixed cases (should default to Arabic)
        ("Hello مرحبا", "ar"),
        ("I am sad أشعر بالحزن", "ar"),
        
        # Edge cases
        ("", "ar"),  # Empty string should default to Arabic
        ("123 456 789", "ar"),  # Numbers only should default to Arabic
        ("!@#$%^&*()", "ar"),  # Punctuation only should default to Arabic
    ]
    
    print("\nTesting language detection:")
    print("-" * 30)
    
    passed = 0
    failed = 0
    
    for text, expected_lang in test_cases:
        detected_lang = therapist_ai.detect_language(text)
        
        if detected_lang == expected_lang:
            print(f"✅ '{text}' -> {detected_lang} (expected: {expected_lang})")
            passed += 1
        else:
            print(f"❌ '{text}' -> {detected_lang} (expected: {expected_lang})")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All language detection tests passed!")
        return True
    else:
        print("⚠️  Some language detection tests failed")
        return False

def test_voice_configuration():
    """Test voice configuration for different languages"""
    print("\nTesting Voice Configuration")
    print("=" * 50)
    
    try:
        therapist_ai = OmaniTherapistAI()
        
        # Test Arabic voices
        ar_male = therapist_ai.voices['ar']['male']
        ar_female = therapist_ai.voices['ar']['female']
        
        # Test English voices
        en_male = therapist_ai.voices['en']['male']
        en_female = therapist_ai.voices['en']['female']
        
        print(f"✅ Arabic Male Voice: {ar_male}")
        print(f"✅ Arabic Female Voice: {ar_female}")
        print(f"✅ English Male Voice: {en_male}")
        print(f"✅ English Female Voice: {en_female}")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice configuration test failed: {e}")
        return False

def test_system_prompts():
    """Test system prompt selection"""
    print("\nTesting System Prompt Selection")
    print("=" * 50)
    
    try:
        therapist_ai = OmaniTherapistAI()
        
        # Test Arabic system prompt
        if hasattr(therapist_ai, 'system_prompt_arabic'):
            print("✅ Arabic system prompt exists")
        else:
            print("❌ Arabic system prompt missing")
            return False
            
        # Test English system prompt
        if hasattr(therapist_ai, 'system_prompt_english'):
            print("✅ English system prompt exists")
        else:
            print("❌ English system prompt missing")
            return False
            
        # Test default system prompt
        if hasattr(therapist_ai, 'system_prompt'):
            print("✅ Default system prompt exists")
        else:
            print("❌ Default system prompt missing")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ System prompt test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Language Detection and Response System Tests")
    print("=" * 60)
    
    tests = [
        test_language_detection,
        test_voice_configuration,
        test_system_prompts
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test in tests:
        try:
            if test():
                passed_tests += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"FINAL RESULTS: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Language detection system is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 