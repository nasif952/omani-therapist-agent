import azure.cognitiveservices.speech as speechsdk
import time
import os
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv(dotenv_path='../../../.env')  # Look for .env in project root
load_dotenv()  # Also check current directory as fallback

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

print("🎤 Microphone Test for Omani Arabic")
print("=" * 40)

# Test with longer timeout and English first to verify mic works
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Test 1: English (to verify microphone works)
print("\n🇺🇸 Test 1: English (to verify microphone)")
speech_config.speech_recognition_language = "en-US"
audio_config = speechsdk.AudioConfig(use_default_microphone=True)
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

print("Say 'Hello world' in English...")
result = recognizer.recognize_once()
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print(f"✅ English recognized: {result.text}")
    print("✅ Microphone is working!")
else:
    print(f"❌ English test failed: {result.reason}")

# Test 2: Omani Arabic
print("\n🇴🇲 Test 2: Omani Arabic")
speech_config.speech_recognition_language = "ar-OM"
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

print("Say 'مرحبا كيف حالك' (Hello, how are you) in Arabic...")
print("⏳ Listening for 10 seconds...")

result = recognizer.recognize_once()
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print(f"✅ Arabic recognized: {result.text}")
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("❌ No Arabic speech detected")
    print("💡 Try:")
    print("   - Speaking closer to microphone")
    print("   - Speaking louder")
    print("   - Check if microphone is muted")
elif result.reason == speechsdk.ResultReason.Canceled:
    details = result.cancellation_details
    print(f"❌ Canceled: {details.reason}")
    if details.reason == speechsdk.CancellationReason.Error:
        print(f"Error: {details.error_details}")

print("\n📊 Summary:")
print("- If English worked but Arabic didn't: microphone is fine, try speaking Arabic louder")
print("- If neither worked: check microphone settings in Windows")
print("- If both worked: your setup is perfect! 🎉") 