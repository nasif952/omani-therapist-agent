# Omani Therapist AI - Complete Voice Conversation System

## 🇴🇲 Overview

This is a complete AI-powered conversational therapy system that speaks and understands Omani Arabic. It integrates:

- **Speech-to-Text (STT)**: Azure Cognitive Services for Omani Arabic recognition
- **AI Conversation**: OpenAI GPT-4o with Anthropic Claude fallback
- **Text-to-Speech (TTS)**: Native Omani Arabic voices with emotional control
- **Session Management**: Conversation memory and transcript saving
- **Cultural Sensitivity**: Therapeutic responses adapted for Omani culture

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in this directory:

```bash
# Required: Azure Speech Services
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=uaenorth

# Required: AI Services (at least one)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 3. Run the Demo

```bash
# Text-based demo (no microphone required)
python demo_ai_conversation.py --mode text

# Voice-based demo (full conversation)
python demo_ai_conversation.py --mode voice

# Quick AI test (no speech)
python demo_ai_conversation.py --mode test-ai

# Check dependencies
python demo_ai_conversation.py --mode check-deps
```

## 📋 Features

### 🎤 Speech Recognition
- **Native Omani Arabic** (ar-OM) recognition
- **High accuracy** with cultural terminology
- **Automatic error handling** and retry logic
- **Microphone permission** detection

### 🤖 AI Conversation
- **OpenAI GPT-4o** as primary AI engine
- **Anthropic Claude** as intelligent fallback
- **Therapeutic system prompt** for culturally-sensitive responses
- **Session memory** maintains conversation context
- **Omani cultural awareness** in responses

### 🔊 Text-to-Speech
- **Native Omani voices**: Abdullah (male) and Aysha (female)
- **Emotional control**: calm, encouraging, excited, sad, neutral
- **48kHz high-quality** audio output
- **SSML support** for advanced speech control
- **Real-time playback** with pygame

### 💾 Session Management
- **Conversation memory** with configurable history length
- **Automatic transcript** saving after each session
- **Session reset** capability
- **Structured logging** for debugging

## 🎭 Demo Modes

### Text Mode (Recommended for Testing)
```bash
python demo_ai_conversation.py --mode text
```
- Type Arabic text instead of speaking
- Perfect for testing without microphone
- AI responds with both text and speech

### Voice Mode (Full Experience)
```bash
python demo_ai_conversation.py --mode voice
```
- Complete voice conversation experience
- Speak in Arabic, AI responds in Omani Arabic
- Requires working microphone

### Test Mode (Quick AI Testing)
```bash
python demo_ai_conversation.py --mode test-ai
```
- Tests AI responses only (no speech)
- Quick verification of AI connectivity
- Good for troubleshooting API issues

## 🔧 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Microphone    │───▶│  Azure STT      │───▶│  User Text      │
│   (Arabic)      │    │  (ar-OM)        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Speakers      │◀───│  Azure TTS      │◀───│  AI Response    │
│   (Omani)       │    │  (ar-OM)        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        ▲
                                                        │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   OpenAI        │───▶│  Session        │───▶│  Context        │
│   GPT-4o        │    │  Memory         │    │  Management     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                                              ▲
         ▼                                              │
┌─────────────────┐                           ┌─────────────────┐
│   Claude        │                           │   Therapeutic   │
│   (Fallback)    │                           │   System Prompt │
└─────────────────┘                           └─────────────────┘
```

## 🛠️ Configuration

### Azure Speech Services
```python
# In omani_therapist_ai.py
self.azure_speech_key = os.getenv('AZURE_SPEECH_KEY')
self.azure_region = os.getenv('AZURE_SPEECH_REGION', 'uaenorth')
```

### AI Services
```python
# Primary: OpenAI GPT-4o
self.openai_api_key = os.getenv('OPENAI_API_KEY')

# Fallback: Anthropic Claude
self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
```

### Voice Settings
```python
# Available voices
self.voices = {
    'male': 'ar-OM-AbdullahNeural',
    'female': 'ar-OM-AyshaNeural'
}

# Default settings
self.default_voice_gender = "female"
self.default_emotion = "neutral"
```

## 🎯 Usage Examples

### Basic Conversation
```python
from omani_therapist_ai import OmaniTherapistAI

# Initialize the system
ai = OmaniTherapistAI()

# Start conversation loop
ai.run_conversation_loop()
```

### Custom Configuration
```python
# Initialize with custom settings
ai = OmaniTherapistAI()
ai.default_voice_gender = "male"
ai.default_emotion = "calm"
ai.max_memory_turns = 15

# Get AI response
response = ai.get_ai_response("كيف حالك اليوم؟")

# Speak with custom voice
ai.speak_text(response, voice_gender="male", emotion="encouraging")
```

### Session Management
```python
# Save transcript
transcript_file = ai.save_session_transcript("my_session.txt")

# Reset conversation
ai.reset_session()
```

## 📱 Voice Commands

### Arabic Commands
- **End session**: "انتهى", "وداعا"
- **Reset conversation**: "بداية جديدة"
- **Continue**: Any Arabic text

### English Commands (also supported)
- **End session**: "exit", "bye"
- **Reset conversation**: "reset", "start over"

## 🔍 Troubleshooting

### Common Issues

#### 1. Azure Authentication Error (401)
```
🚨 Authentication error - please check Azure credentials
```
**Solution**: Verify your `AZURE_SPEECH_KEY` in the `.env` file

#### 2. Microphone Permission Issue
```
🚨 Microphone permission issue - check Windows settings
```
**Solution**: 
- Check Windows microphone privacy settings
- Ensure microphone is not muted
- Try running as administrator

#### 3. No Speech Detected
```
❌ No speech detected. Try speaking louder or closer to the microphone.
```
**Solution**:
- Speak closer to the microphone
- Increase microphone volume
- Try the text demo mode first

#### 4. AI API Errors
```
🚨 Failed to get AI response
```
**Solution**:
- Check your OpenAI/Anthropic API keys
- Verify internet connectivity
- Check API quotas and billing

### Debug Mode
```bash
# Enable verbose logging
export PYTHONPATH=.
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from omani_therapist_ai import OmaniTherapistAI
ai = OmaniTherapistAI()
ai.run_conversation_loop()
"
```

## 🧪 Testing

### 1. Check Dependencies
```bash
python demo_ai_conversation.py --mode check-deps
```

### 2. Test AI Only
```bash
python demo_ai_conversation.py --mode test-ai
```

### 3. Test with Text Input
```bash
python demo_ai_conversation.py --mode text
```

### 4. Full Voice Test
```bash
python demo_ai_conversation.py --mode voice
```

## 📄 Output Files

### Session Transcripts
- **Format**: `therapy_session_YYYYMMDD_HHMMSS.txt`
- **Location**: Current directory
- **Content**: Complete conversation history with timestamps

### Example Transcript
```
Omani Therapist AI - Session Transcript
==================================================
Session Date: 2024-01-15 14:30:22
Total Messages: 6
==================================================

[1] USER (14:30:25)
مرحبا، كيف حالك؟

[2] ASSISTANT (14:30:28)
أهلاً وسهلاً بك! أنا بخير الحمد لله. كيف أقدر أساعدك اليوم؟
    Voice: female, Emotion: neutral
```

## 🔐 Security

### Environment Variables
- **Never commit** `.env` files to version control
- **Use strong** API keys
- **Rotate keys** regularly
- **Monitor usage** for unusual activity

### Audio Data
- **No audio recording** is saved to disk
- **Real-time processing** only
- **Memory cleared** after each session
- **Transcripts saved** as text only

## 🌍 Cultural Sensitivity

The AI is specifically trained to:
- **Respect Omani culture** and traditions
- **Use appropriate Islamic** references when relevant
- **Maintain professional** therapeutic boundaries
- **Encourage professional help** for serious issues
- **Use authentic Omani dialect** expressions

## 📚 API Reference

### OmaniTherapistAI Class

#### Methods

- `get_user_speech(timeout_seconds=10)`: Capture speech input
- `get_ai_response(user_input)`: Get AI response with fallback
- `speak_text(text, voice_gender="female", emotion="neutral")`: Text-to-speech
- `save_session_transcript(filename=None)`: Save conversation
- `reset_session()`: Clear conversation memory
- `run_conversation_loop()`: Main conversation loop

#### Properties

- `session_memory`: List of conversation messages
- `voices`: Available voice options
- `default_voice_gender`: Default voice setting
- `default_emotion`: Default emotion setting
- `max_memory_turns`: Context memory limit

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Test** thoroughly with Arabic input
4. **Submit** a pull request

## 📜 License

This project is part of the Omani Therapist Voice Bot technical assessment.

## 🆘 Support

For issues or questions:
1. Check the **troubleshooting** section
2. Review the **logs** for detailed error messages
3. Test with **different modes** to isolate issues
4. Ensure all **dependencies** are correctly installed

---

**Made with ❤️ for the Omani healthcare community** 