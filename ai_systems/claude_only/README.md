# Omani Therapist AI - Claude Opus 4 Only Edition

This folder contains the **Claude-only version** of the Omani Therapist AI system.

## 🇴🇲 Overview

This is a pure Claude Opus 4 implementation that provides:

- **Claude Opus 4** as the primary AI model (claude-opus-4-20250514)
- **Claude 3.5 Sonnet** as automatic fallback if Opus 4 unavailable
- **Native Omani Arabic** speech recognition and synthesis
- **Performance timing** measurements from speech to voice response
- **Culturally-sensitive** therapeutic conversations
- **Session management** with transcripts

## 📁 Files

### Core System
- **`omani_therapist_ai_onlyclaude.py`** - Main Claude-only AI system (771 lines)
- **`demo_claude_conversation.py`** - Demo script with multiple modes (280 lines)

## 🚀 Quick Start

### 1. Set Up Environment
Create a `.env` file in the project root with:
```bash
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=uaenorth
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 2. Install Dependencies
```bash
pip install anthropic azure-cognitiveservices-speech pygame python-dotenv
```

### 3. Run the System

#### Text Mode (No Microphone)
```bash
python demo_claude_conversation.py --mode text
```

#### Voice Mode (Full Conversation)
```bash
python demo_claude_conversation.py --mode voice
```

#### Quick AI Test
```bash
python demo_claude_conversation.py --mode test-ai
```

#### Check Dependencies
```bash
python demo_claude_conversation.py --mode check-deps
```

## 🎯 Features

### Claude Opus 4 Integration
- **Primary Model**: claude-opus-4-20250514
- **Fallback Model**: claude-3-5-sonnet-20241022
- **Temperature**: 0.7 for natural conversations
- **Max Tokens**: 600 for detailed responses

### Arabic Speech Support
- **STT**: Omani Arabic (ar-OM) recognition
- **TTS**: Native Omani voices (Abdullah & Aysha)
- **Audio Quality**: 48kHz uncompressed PCM

### Performance Timing
- **Speech Recognition**: Measures STT latency
- **AI Processing**: Tracks Claude response time
- **TTS Synthesis**: Monitors voice generation
- **Total Latency**: End-to-end conversation timing

### Session Management
- **Memory**: Maintains last 10 conversation turns
- **Transcripts**: Auto-saves with timing statistics
- **Reset**: Command to start fresh conversations

## 🎤 Voice Commands

### Arabic Commands
- **End session**: "انتهى", "وداعا"
- **Reset conversation**: "بداية جديدة"

### English Commands
- **End session**: "exit", "bye"
- **Reset conversation**: "reset", "start over"

## 📊 Performance

Typical performance metrics:
- **STT**: ~0.1-0.5 seconds
- **Claude Opus 4**: ~1.5-8 seconds
- **TTS**: ~0.5-2 seconds
- **Total Latency**: ~2-10 seconds

## 🔧 Configuration

### Voice Settings
```python
# Available voices
voices = {
    'male': 'ar-OM-AbdullahNeural',
    'female': 'ar-OM-AyshaNeural'
}

# Default settings
default_voice_gender = "female"
default_emotion = "neutral"
```

### Memory Settings
```python
max_memory_turns = 10  # Keep last 10 exchanges
```

## 🛠️ Troubleshooting

### Common Issues

1. **No Voice Output**
   - Check Azure Speech credentials
   - Verify speakers/headphones are working
   - Ensure uaenorth region is supported

2. **Claude API Errors**
   - Verify Anthropic API key
   - Check internet connection
   - Monitor API quotas

3. **Microphone Issues**
   - Check Windows microphone permissions
   - Ensure microphone is not muted
   - Try text mode first

## 📄 Output Files

- **Session Transcripts**: `therapy_session_claude_YYYYMMDD_HHMMSS.txt`
- **Location**: Current directory
- **Content**: Complete conversation with timing statistics

## 🌍 Cultural Sensitivity

The system is specifically designed for:
- **Omani Arabic dialect** and cultural context
- **Islamic values** and family-oriented approach
- **Professional therapeutic** boundaries
- **Local healthcare** referrals when needed

## 🔐 Security

- **No audio recording** saved to disk
- **Real-time processing** only
- **Transcripts** contain text only
- **API keys** managed via environment variables

---

**Ready to use!** The Claude-only system provides reliable, culturally-sensitive therapeutic conversations in Omani Arabic with comprehensive performance monitoring. 