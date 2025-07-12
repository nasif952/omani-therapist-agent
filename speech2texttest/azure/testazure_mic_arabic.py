import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment variables
speech_key = os.getenv('AZURE_SPEECH_KEY')
service_region = os.getenv('AZURE_SPEECH_REGION', 'uaenorth')

# Try backup key if primary not found
if not speech_key:
    speech_key = os.getenv('AZURE_SPEECH_KEY_BACKUP')

if not speech_key:
    print("❌ Error: Azure Speech Key not found!")
    print("Please set AZURE_SPEECH_KEY in your environment variables or .env file")
    print("Example: AZURE_SPEECH_KEY=your_key_here")
    exit(1)

print(f"🔑 Using key ending in: ...{speech_key[-4:]}")
print(f"🌍 Region: {service_region}")

try:
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = "ar-OM"  # Omani Arabic

    # Use the default microphone as audio input
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("🎤 Say something in Omani Arabic (or play a test audio near the mic)...")
    print("⏳ Listening for speech...")

    result = speech_recognizer.recognize_once()
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"✅ Recognized: {result.text}")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("❌ No speech could be recognized")
        print("💡 Try speaking louder or closer to the microphone")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"❌ Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"🚨 Error details: {cancellation_details.error_details}")
            if "401" in str(cancellation_details.error_details):
                print("💡 This is the same credential issue we saw with TTS!")
                print("💡 Check Azure Portal to regenerate keys")
            elif "microphone" in str(cancellation_details.error_details).lower():
                print("💡 Check microphone permissions in Windows Settings")
    else:
        print(f"❓ Unexpected result: {result.reason}")
        
except Exception as e:
    print(f"💥 Exception occurred: {e}")
    print("📋 Common issues:")
    print("   1. Invalid Azure credentials")
    print("   2. Microphone permission denied") 
    print("   3. Network connectivity problems")
    print("   4. Azure service temporarily unavailable")

print("\n🔧 To run this test: python test_mic_fixed.py") 