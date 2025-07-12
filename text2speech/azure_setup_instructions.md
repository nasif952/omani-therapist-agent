# Azure Text-to-Speech Setup Instructions

This guide will help you set up Azure Speech Services to test Omani Arabic TTS voices.

## 1. Create Azure Speech Services Resource

### Step 1: Azure Account
- Go to [Azure Portal](https://portal.azure.com)
- Sign in or create a free Azure account
- If new, you'll get $200 free credit for 30 days

### Step 2: Create Speech Service
1. Click "Create a resource" in Azure Portal
2. Search for "Speech Services" or "Cognitive Services"
3. Click "Speech Services" → "Create"
4. Fill in the details:
   - **Subscription**: Select your subscription
   - **Resource Group**: Create new or use existing
   - **Region**: Choose a region (recommended: East US, West Europe, or Southeast Asia)
   - **Name**: Give your service a unique name
   - **Pricing Tier**: F0 (Free) for testing, or S0 (Standard) for production

### Step 3: Get Your Credentials
1. After creation, go to your Speech Services resource
2. In the left menu, click "Keys and Endpoint"
3. Copy:
   - **Key 1** (your speech key)
   - **Region** (where you deployed the service)

## 2. Install Dependencies

### Option A: Using pip
```bash
pip install -r requirements.txt
```

### Option B: Install directly
```bash
pip install azure-cognitiveservices-speech>=1.34.0
```

## 3. Set Up Credentials

### Option A: Environment Variables (Recommended)

#### Windows (PowerShell):
```powershell
$env:AZURE_SPEECH_KEY = "your-speech-key-here"
$env:AZURE_SPEECH_REGION = "your-region-here"
```

#### Windows (Command Prompt):
```cmd
set AZURE_SPEECH_KEY=your-speech-key-here
set AZURE_SPEECH_REGION=your-region-here
```

#### Linux/macOS:
```bash
export AZURE_SPEECH_KEY="your-speech-key-here"
export AZURE_SPEECH_REGION="your-region-here"
```

### Option B: Edit the Script Directly
Open `test_azure_omani_tts.py` and uncomment these lines in the `main()` function:
```python
speech_key = "YOUR_AZURE_SPEECH_KEY"
service_region = "eastus"  # or your preferred region
```

## 4. Run the Test

```bash
python test_azure_omani_tts.py
```

## 5. What the Test Does

The script will:
1. Test both Omani Arabic voices (male and female)
2. Generate audio samples for various scenarios:
   - General greetings
   - Therapy/medical contexts
   - Omani-specific phrases
   - Emotional support language
   - Complex medical terminology
3. Test SSML (Speech Synthesis Markup Language) capabilities
4. Save all audio files to `omani_tts_samples/` folder
5. Generate a test results JSON file

## 6. Expected Output

You should see:
- ✅ Success messages for each audio generation
- Audio files saved in `omani_tts_samples/` folder
- Test summary with success/failure counts
- Instructions for evaluating the audio quality

## 7. Audio File Naming Convention

Files are named as: `{test_type}_{gender}_omani.wav` (Highest quality WAV format)

Examples:
- `greeting_female_omani.wav`
- `therapy_intro_male_omani.wav`
- `omani_specific_female_omani.wav`
- `ssml_test_male_omani.wav`

## 8. Troubleshooting

### Common Issues:

#### "Speech Key not found" Error
- Verify your environment variables are set correctly
- Try restarting your terminal/command prompt
- Check if you're using the correct variable names

#### "Authentication failed" Error
- Verify your speech key is correct (no extra spaces)
- Check if your Azure subscription is active
- Ensure the region matches where you created the service

#### "Region not supported" Error
- Try different regions: `eastus`, `westeurope`, `southeastasia`
- Verify the region name format (lowercase, no spaces)

#### Network/Connection Issues
- Check your internet connection
- Try from a different network if behind corporate firewall
- Verify Azure services aren't blocked

### Audio Quality Issues
- Files are generated in 48kHz WAV format for HIGHEST quality
- Uncompressed audio ensures no quality loss
- If audio is poor quality, try different Azure regions
- Compare male vs female voices for your use case

## 9. Next Steps

After testing:
1. Listen to all generated audio samples
2. Evaluate naturalness for Omani dialect
3. Test with your specific therapy/medical content
4. Consider voice cloning options if needed
5. Plan integration into your application

## 10. Pricing Information

### Free Tier (F0):
- 500,000 characters per month
- Good for testing and small applications

### Standard Tier (S0):
- Neural voices: $16 per 1 million characters
- Standard voices: $4 per 1 million characters
- No monthly limits

### Cost Estimation:
- Average therapy session (500 words): ~2,500 characters
- 100 sessions/month ≈ 250,000 characters
- Cost: ~$4-8/month for moderate usage

## Support

If you encounter issues:
1. Check the [Azure Speech Services documentation](https://docs.microsoft.com/azure/cognitive-services/speech-service/)
2. Review the error messages in the test output
3. Verify your Azure portal settings
4. Contact Azure support if needed 