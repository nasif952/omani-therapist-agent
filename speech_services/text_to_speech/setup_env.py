#!/usr/bin/env python3
"""
Simple .env Setup Script
Automatically creates .env file from template
"""

import os
import shutil

print("🔧 Setting up .env file for Azure TTS")
print("=" * 40)

# Check if env_template.txt exists
if os.path.exists('env_template.txt'):
    print("✅ Found env_template.txt")
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️ .env file already exists")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower().strip()
        if overwrite != 'y':
            print("❌ Setup cancelled")
            exit()
    
    # Copy template to .env
    try:
        shutil.copy2('env_template.txt', '.env')
        print("✅ Successfully created .env file")
        
        # Verify the content
        with open('.env', 'r') as f:
            content = f.read()
            
        if 'AZURE_SPEECH_KEY=' in content and 'AM1Kx' in content:
            print("✅ .env file contains Azure credentials")
            print("🎉 Setup complete! You can now run:")
            print("   python test_azure_omani_tts.py")
        else:
            print("❌ .env file seems incomplete")
            print("Please check the .env file content")
            
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        
else:
    print("❌ env_template.txt not found")
    print("Please make sure you're in the text2speech directory")

print("\n" + "=" * 40) 