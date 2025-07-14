#!/usr/bin/env python3
"""
Test script for webapp emotion integration
Tests that the webapp now properly detects emotions from AI responses and applies them to TTS
"""
import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv(dotenv_path='../.env')

# Add current directory to path
sys.path.append('.')

try:
    from omani_therapist_ai import OmaniTherapistAI
    
    print("🎭 Webapp Emotion Integration Test")
    print("=" * 50)
    
    # Initialize AI
    print("1. Initializing AI system...")
    ai = OmaniTherapistAI()
    print("✅ AI system initialized")
    
    # Test emotion detection on various AI response patterns
    test_responses = {
        'encouraging_arabic': "أنت قادر على تجاوز هذه المشكلة! لا تقلق، إن شاء الله بيكون خير. أنت قوي وتستطيع التعامل مع هذا الموقف.",
        'encouraging_english': "You can overcome this challenge! Don't worry, you're doing great and I believe in you completely.",
        
        'excited_arabic': "مبروك! هذا إنجاز رائع جداً! ما شاء الله عليك، تطور ممتاز!",
        'excited_english': "Congratulations! This is fantastic progress! I'm so proud of your breakthrough!",
        
        'sad_arabic': "أتفهم ألمك وأعرف أن هذا صعب عليك. أحس بيك والله يصبرك على هذه المحنة.",
        'sad_english': "I understand your pain and I know this is really difficult for you. I'm here with you through this.",
        
        'calm_arabic': "خذ نفس عميق واهدأ. بالهدوء والتأمل راح تقدر تتعامل مع الموقف خطوة بخطوة.",
        'calm_english': "Take a deep breath and relax. With calmness and mindfulness, you can handle this step by step.",
        
        'neutral_arabic': "هذا موضوع مهم ويحتاج تفكير. يمكننا مناقشة الخيارات المتاحة لك.",
        'neutral_english': "This is an important topic that requires consideration. We can discuss the available options."
    }
    
    print("\n2. Testing emotion detection from AI responses:")
    print("-" * 50)
    
    for test_name, response_text in test_responses.items():
        detected_emotion = ai.detect_emotion_from_text(response_text)
        expected_emotion = test_name.split('_')[0]  # Extract expected emotion from test name
        
        print(f"\n🔍 Test: {test_name}")
        print(f"📝 Response: {response_text[:60]}...")
        print(f"🎯 Expected: {expected_emotion}")
        print(f"✅ Detected: {detected_emotion}")
        
        # Check if detection matches expectation
        if detected_emotion == expected_emotion:
            print("✅ PASS - Emotion detection correct")
        else:
            print("❌ FAIL - Emotion detection mismatch")
    
    print("\n3. Testing TTS with detected emotions:")
    print("-" * 50)
    
    # Test a few key examples with actual TTS generation
    key_tests = [
        ("encouraging_arabic", test_responses['encouraging_arabic']),
        ("excited_english", test_responses['excited_english']),
        ("sad_arabic", test_responses['sad_arabic']),
        ("calm_english", test_responses['calm_english'])
    ]
    
    for test_name, text in key_tests:
        print(f"\n🎵 Generating TTS for: {test_name}")
        
        # Detect emotion
        detected_emotion = ai.detect_emotion_from_text(text)
        print(f"🎭 Emotion: {detected_emotion}")
        
        # Generate TTS with detected emotion
        language = "ar" if "arabic" in test_name else "en"
        audio_bytes = ai.speak_text(
            text,
            emotion=detected_emotion,
            return_bytes=True,
            language=language
        )
        
        if audio_bytes and isinstance(audio_bytes, bytes):
            print(f"✅ TTS generated: {len(audio_bytes)} bytes")
            
            # Save audio file for testing
            filename = f"test_webapp_emotion_{test_name}.wav"
            with open(filename, 'wb') as f:
                f.write(audio_bytes)
            print(f"💾 Audio saved: {filename}")
        else:
            print("❌ TTS generation failed")
    
    print("\n🎉 Webapp emotion integration test completed!")
    print("📁 Audio files generated for manual verification.")
    print("🔗 These audio files should demonstrate different emotional prosody.")

except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc() 