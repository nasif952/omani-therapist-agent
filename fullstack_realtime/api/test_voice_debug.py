#!/usr/bin/env python3
"""
Debug script for voice processing issues
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
    
    print("🔧 Voice Processing Debug Script")
    print("=" * 50)
    
    # Initialize AI
    print("1. Initializing AI system...")
    ai = OmaniTherapistAI()
    print("✅ AI system initialized")
    
    # Test text processing first
    print("\n2. Testing text processing...")
    try:
        from main import TimingMetrics
        import time
        
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
        
        response = ai.get_ai_response("Hello, this is a test", timing)
        if response:
            print("✅ Text processing works")
            print(f"Response: {response[:100]}...")
        else:
            print("❌ Text processing failed")
            
    except Exception as e:
        print(f"❌ Text processing error: {e}")
    
    # Test TTS
    print("\n3. Testing TTS...")
    try:
        tts_result = ai.speak_text("Test message", return_bytes=True)
        if isinstance(tts_result, (bytes, bytearray)) and len(tts_result) > 0:
            print("✅ TTS works")
            print(f"TTS audio size: {len(tts_result)} bytes")
        else:
            print("❌ TTS failed")
            print(f"TTS result type: {type(tts_result)}")
    except Exception as e:
        print(f"❌ TTS error: {e}")
    
    # Test audio format detection
    print("\n4. Testing audio format detection...")
    try:
        # Test WebM signature
        webm_header = b'\x1a\x45\xdf\xa3' + b'\x00' * 20
        detected = ai._detect_audio_format(webm_header)
        print(f"WebM detection: {detected}")
        
        # Test WAV signature  
        wav_header = b'RIFF' + b'\x00' * 4 + b'WAVE' + b'\x00' * 20
        detected = ai._detect_audio_format(wav_header)
        print(f"WAV detection: {detected}")
        
    except Exception as e:
        print(f"❌ Audio format detection error: {e}")
    
    print("\n" + "=" * 50)
    print("Debug complete!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ General error: {e}") 