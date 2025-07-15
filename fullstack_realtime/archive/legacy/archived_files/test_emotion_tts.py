#!/usr/bin/env python3
"""
Test script for emotion-based TTS functionality
Tests if different emotions produce different speech patterns (rate/pitch)
"""
import os
import sys
import tempfile
from dotenv import load_dotenv

# Load environment
load_dotenv(dotenv_path='../.env')

# Add current directory to path
sys.path.append('.')

try:
    from omani_therapist_ai import OmaniTherapistAI
    
    print("🎭 Emotion-Based TTS Test Script")
    print("=" * 50)
    
    # Initialize AI
    print("1. Initializing AI system...")
    ai = OmaniTherapistAI()
    print("✅ AI system initialized")
    
    # Test message in both languages
    test_messages = {
        'ar': "هذا اختبار للعواطف المختلفة",  # "This is a test for different emotions"
        'en': "This is a test for different emotions"
    }
    
    # Test all emotions
    emotions_to_test = ['calm', 'encouraging', 'excited', 'sad', 'neutral']
    
    print("\n2. Testing emotion-based TTS...")
    print("Each emotion should produce different speech characteristics:")
    print("- calm: slow rate, low pitch")
    print("- encouraging: medium rate, medium pitch") 
    print("- excited: fast rate, high pitch")
    print("- sad: x-slow rate, x-low pitch")
    print("- neutral: medium rate, medium pitch")
    print()
    
    for language in ['ar', 'en']:
        print(f"\n--- Testing {language.upper()} language ---")
        
        for emotion in emotions_to_test:
            try:
                print(f"Testing emotion: {emotion}")
                
                # Generate TTS with specific emotion
                audio_bytes = ai.speak_text(
                    text=test_messages[language],
                    emotion=emotion,
                    language=language,
                    return_bytes=True
                )
                
                if isinstance(audio_bytes, (bytes, bytearray)) and len(audio_bytes) > 0:
                    print(f"  ✅ {emotion}: Audio generated ({len(audio_bytes)} bytes)")
                    
                    # Save audio file for manual testing (optional)
                    filename = f"test_emotion_{emotion}_{language}.wav"
                    with open(filename, 'wb') as f:
                        f.write(audio_bytes)
                    print(f"  💾 Saved as: {filename}")
                    
                else:
                    print(f"  ❌ {emotion}: Failed to generate audio")
                    
            except Exception as e:
                print(f"  ❌ {emotion}: Error - {e}")
    
    print("\n3. Testing SSML generation...")
    # Test SSML creation directly
    for emotion in emotions_to_test:
        try:
            ssml = ai._create_ssml_text(
                text="Test message for SSML",
                emotion=emotion,
                language="ar"
            )
            print(f"✅ {emotion}: SSML generated")
            # Print a snippet to verify prosody settings
            if 'prosody' in ssml:
                prosody_start = ssml.find('<prosody')
                prosody_end = ssml.find('>', prosody_start) + 1
                prosody_tag = ssml[prosody_start:prosody_end]
                print(f"  Prosody: {prosody_tag}")
            
        except Exception as e:
            print(f"❌ {emotion}: SSML generation failed - {e}")
    
    print("\n" + "=" * 50)
    print("🎭 Emotion TTS Test Complete!")
    print("\nTo verify emotions are working:")
    print("1. Check the console output above for successful audio generation")
    print("2. Listen to the generated .wav files (if saved)")
    print("3. Compare the prosody settings in SSML output")
    print("4. Each emotion should have different rate/pitch combinations")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ General error: {e}") 