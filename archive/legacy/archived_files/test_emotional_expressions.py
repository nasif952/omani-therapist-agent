#!/usr/bin/env python3
"""
Test script for emotional expressions in TTS
Tests support for sighs, ellipsis, and natural hesitations
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
    
    print("🎭 Emotional Expressions TTS Test")
    print("=" * 50)
    
    # Initialize AI
    print("1. Initializing AI system...")
    ai = OmaniTherapistAI()
    print("✅ AI system initialized")
    
    # Test messages with emotional expressions
    test_expressions = {
        'ellipsis': "I don't know... maybe we should try something different.",
        'sigh': "Well <sigh> I guess that's just how it is.",
        'sigh_asterisk': "I tried my best *sigh* but it didn't work out.",
        'sigh_parentheses': "This is really difficult (sigh) to understand.",
        'long_pause': "Wait____let me think about this.",
        'hesitation': "Umm... I think... ah... yes, that might work.",
        'multiple_dots': "So..... what do you think about this idea?",
        'complex': "I was thinking... *sigh*... maybe we could... umm... try a different approach?"
    }
    
    print("\n2. Testing emotional expressions...")
    
    for expression_type, text in test_expressions.items():
        try:
            print(f"\nTesting: {expression_type}")
            print(f"Input: {text}")
            
            # Generate TTS with emotional expression processing
            audio_bytes = ai.speak_text(
                text=text,
                emotion="neutral",
                language="en",
                return_bytes=True
            )
            
            if isinstance(audio_bytes, (bytes, bytearray)) and len(audio_bytes) > 0:
                print(f"  ✅ Generated audio ({len(audio_bytes)} bytes)")
                
                # Save audio file
                filename = f"test_expression_{expression_type}.wav"
                with open(filename, 'wb') as f:
                    f.write(audio_bytes)
                print(f"  💾 Saved as: {filename}")
                
                # Show how the text was processed
                processed_text = ai._add_natural_pauses(text, "neutral")
                print(f"  📝 Processed SSML includes: {processed_text[:100]}...")
                
            else:
                print(f"  ❌ Failed to generate audio")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n3. Testing with different emotions...")
    emotional_text = "I feel... *sigh*... really tired today..."
    
    for emotion in ['sad', 'calm', 'neutral']:
        try:
            print(f"\nTesting emotion: {emotion}")
            
            audio_bytes = ai.speak_text(
                text=emotional_text,
                emotion=emotion,
                language="en",
                return_bytes=True
            )
            
            if isinstance(audio_bytes, (bytes, bytearray)) and len(audio_bytes) > 0:
                filename = f"test_emotional_expression_{emotion}.wav"
                with open(filename, 'wb') as f:
                    f.write(audio_bytes)
                print(f"  ✅ {emotion}: Saved as {filename}")
            
        except Exception as e:
            print(f"  ❌ {emotion}: Error - {e}")
    
    print("\n" + "=" * 50)
    print("🎭 Emotional Expressions Test Complete!")
    print("\nSupported expressions:")
    print("- ... (ellipsis) → natural pause")
    print("- ___ (underscores) → pause")
    print("- <sigh>, *sigh*, (sigh) → breathing pause")
    print("- umm, ah → hesitation with pauses")
    print("- Combines with emotion settings for natural speech")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ General error: {e}") 