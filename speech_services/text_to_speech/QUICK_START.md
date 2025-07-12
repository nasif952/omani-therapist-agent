# 🚀 Quick Start Guide - Azure Omani TTS Testing

## ⚡ 30-Second Setup

### Step 1: Install Dependencies
```bash
cd text2speech
pip install -r requirements.txt
```

### Step 2: Set Up Credentials

**Easy .env Setup (Recommended):**
```bash
# Copy the template and it will have your credentials
copy env_template.txt .env

# That's it! The .env file is already configured with your Azure keys
```

**Alternative - Manual Environment Variables:**
```bash
# Windows Command Prompt
set AZURE_SPEECH_KEY=your_key_here
set AZURE_SPEECH_REGION=uaenorth

# Windows PowerShell
$env:AZURE_SPEECH_KEY = "your_key_here"
$env:AZURE_SPEECH_REGION = "uaenorth"
```

### Step 3: Test Your Setup
```bash
# Run comprehensive test (generates 14+ audio samples)
python test_azure_omani_tts.py

# Run interactive therapy demo
python therapy_tts_example.py
```

## 🎯 What You'll Get

### Audio Samples Generated:
- ✅ `greeting_female_omani.wav` - Basic greeting
- ✅ `therapy_intro_male_omani.wav` - Therapy introduction  
- ✅ `omani_specific_female_omani.wav` - Omani dialect phrases
- ✅ `medical_terms_male_omani.wav` - Medical terminology
- ✅ `emotional_support_female_omani.wav` - Supportive language
- ✅ `ssml_test_male_omani.wav` - Advanced voice control
- ✅ Plus 8+ more samples for evaluation

### Quality Features:
- 🔊 **48kHz WAV** - Studio quality, uncompressed
- 🎭 **Neural Voices** - Most natural Azure voices available
- 🇴🇲 **Native Omani** - `ar-OM-AbdullahNeural` & `ar-OM-AyshaNeural`
- 🎚️ **SSML Control** - Emotional expression and pacing

## 🔧 Testing Options

### 1. Comprehensive Test (`test_azure_omani_tts.py`)
- Tests both male and female voices
- 7 different text scenarios
- SSML advanced features
- Automatic audio file generation
- JSON test results log

### 2. Interactive Therapy Demo (`therapy_tts_example.py`)
- Real-time audio playback
- Custom text input
- Therapy session templates
- Emotional tone control (calm, encouraging, excited)
- Session recording capability

## 📁 Output Structure

```
text2speech/
├── omani_tts_samples/           # Generated audio files
│   ├── greeting_female_omani.wav
│   ├── therapy_intro_male_omani.wav
│   ├── ssml_test_female_omani.wav
│   └── test_results.json        # Detailed test log
└── therapy_session_YYYYMMDD/    # Session recordings (optional)
    ├── 01_session_start.wav
    ├── 02_breathing_1.wav
    └── 05_session_end.wav
```

## 🎧 Evaluation Checklist

Listen to the generated audio and evaluate:

### ✅ Pronunciation Quality
- [ ] Omani-specific terms (شلونك؟, يا أهلا وسهلا)
- [ ] Medical terminology accuracy  
- [ ] Arabic diacritics and vowels

### ✅ Naturalness
- [ ] Human-like rhythm and flow
- [ ] Natural pauses and breathing
- [ ] Emotional expressiveness
- [ ] Professional therapy tone

### ✅ Voice Comparison
- [ ] Male vs Female voice preference
- [ ] Clarity and intelligibility
- [ ] Cultural appropriateness for Omani patients

## 🔒 Security Notes

### ✅ Safe for GitHub
- Credentials are in environment variables only
- `.gitignore` protects sensitive files
- No hardcoded keys in source code

### ✅ Local Testing
- Setup scripts for easy local configuration
- Backup key support for reliability
- UAE North region optimized for your location

## 🆘 Troubleshooting

### "Speech Key not found" Error
```bash
# Make sure you have the .env file
copy env_template.txt .env

# Check if .env file exists and has content
dir .env

# Or set manually as environment variable
set AZURE_SPEECH_KEY=your_key_here
set AZURE_SPEECH_REGION=uaenorth
```

### Audio Quality Issues
- Files are generated as 48kHz WAV (highest quality)
- If playback issues occur, try VLC or Windows Media Player
- Check Windows audio drivers are up to date

### Network/Connection Issues  
- Ensure internet connection is stable
- UAE North region should provide fastest response
- Try backup key if primary fails

## 🎉 Next Steps

1. **Listen to all generated samples**
2. **Choose your preferred voice** (male/female)
3. **Test with your own therapy content**
4. **Integrate into your therapy application**
5. **Consider voice customization options**

---

**🏆 You now have the best possible Omani Arabic TTS setup for therapy applications!** 