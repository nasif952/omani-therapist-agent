#!/usr/bin/env python3
"""
Credential Diagnostic Tool
Check if Azure credentials are loading properly
"""

import os
from dotenv import load_dotenv

print("🔍 Azure Credentials Diagnostic Tool")
print("=" * 50)

# Load .env file
print("1. Loading .env file...")
try:
    load_dotenv()
    print("✅ .env file loaded successfully")
except Exception as e:
    print(f"❌ Error loading .env file: {e}")

print("\n2. Checking environment variables...")

# Check for Azure credentials
speech_key = os.getenv('AZURE_SPEECH_KEY')
backup_key = os.getenv('AZURE_SPEECH_KEY_BACKUP')
region = os.getenv('AZURE_SPEECH_REGION')
endpoint = os.getenv('AZURE_SPEECH_ENDPOINT')

print(f"Primary Key: {'✅ Found' if speech_key else '❌ Not found'}")
if speech_key:
    print(f"  - Length: {len(speech_key)} characters")
    print(f"  - Last 4 chars: ...{speech_key[-4:] if len(speech_key) > 4 else speech_key}")

print(f"Backup Key: {'✅ Found' if backup_key else '❌ Not found'}")
if backup_key:
    print(f"  - Length: {len(backup_key)} characters")
    print(f"  - Last 4 chars: ...{backup_key[-4:] if len(backup_key) > 4 else backup_key}")

print(f"Region: {'✅ ' + region if region else '❌ Not found'}")
print(f"Endpoint: {'✅ ' + endpoint if endpoint else '❌ Not found'}")

print("\n3. Checking file structure...")
import glob

# Check for .env files
env_files = glob.glob('.env*')
template_files = glob.glob('env_template*')

print(f".env files found: {env_files}")
print(f"Template files found: {template_files}")

print("\n4. Manual credential test...")
if speech_key or backup_key:
    test_key = speech_key or backup_key
    key_suffix = test_key[-4:] if test_key and len(test_key) > 4 else "N/A"
    print(f"Testing with key ending in: ...{key_suffix}")
    
    # Quick Azure connection test
    try:
        import azure.cognitiveservices.speech as speechsdk
        
        speech_config = speechsdk.SpeechConfig(
            subscription=test_key,
            region=region or 'uaenorth'
        )
        speech_config.speech_synthesis_voice_name = "ar-OM-AyshaNeural"
        
        # Try to create synthesizer (this will validate credentials)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=None
        )
        
        print("✅ Azure SDK initialized successfully")
        print("🔧 Attempting simple synthesis test...")
        
        # Try a very simple synthesis
        result = synthesizer.speak_text_async("مرحبا").get()
        
        if result and result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("✅ Azure TTS test successful!")
        else:
            print(f"❌ Azure TTS test failed: {result.reason if result else 'Unknown error'}")
            if result and result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                if cancellation_details:
                    print(f"   Error details: {cancellation_details.reason}")
                    if hasattr(cancellation_details, 'error_details') and cancellation_details.error_details:
                        print(f"   Error message: {cancellation_details.error_details}")
        
    except Exception as e:
        print(f"❌ Azure SDK error: {e}")
else:
    print("❌ No credentials found to test")

print("\n" + "=" * 50)
print("🚨 TROUBLESHOOTING TIPS:")
print("1. Make sure .env file exists in this directory")
print("2. Check your Azure portal for resource status")
print("3. Verify billing and quotas are active")
print("4. Try using the other key (primary vs backup)")
print("5. Check if your Azure subscription is still active") 