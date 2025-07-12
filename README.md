# Omani Therapist AI - Voice-Based Mental Health Chatbot

A culturally-sensitive, voice-only mental health chatbot system designed specifically for Omani Arabic speakers, featuring real-time conversational AI with <20 second latency.

## 🏗️ Project Structure

```
📁 main project/
├── 🤖 ai_systems/                    # AI Integration Systems
│   ├── main_system/                  # Primary AI system (OpenAI + Claude)
│   │   ├── omani_therapist_ai.py    # Main AI conversation system
│   │   ├── demo_ai_conversation.py  # Demo script with multiple modes
│   │   ├── requirements.txt         # Python dependencies
│   │   └── README.md               # System documentation
│   └── claude_only/                 # Claude-only AI system
│       ├── omani_therapist_ai_onlyclaude.py  # Pure Claude implementation
│       ├── demo_claude_conversation.py       # Claude demo script
│       └── README.md                         # Claude system docs
│
├── 🗣️ speech_services/              # Speech Processing Services
│   ├── text_to_speech/              # TTS Implementation
│   │   ├── azure_setup_instructions.md  # Azure TTS setup guide
│   │   ├── therapy_tts_example.py      # TTS example scripts
│   │   ├── test_azure_omani_tts.py     # TTS testing utilities
│   │   ├── check_credentials.py        # Credential validation
│   │   ├── setup_env.py               # Environment setup
│   │   ├── omani_tts_samples/         # Audio samples
│   │   ├── requirements.txt           # TTS dependencies
│   │   ├── ENV_SETUP_GUIDE.md         # Environment guide
│   │   ├── QUICK_START.md             # Quick start guide
│   │   └── TTS services comparison.md  # Service comparison
│   └── speech_to_text/              # STT Implementation
│       ├── azure/                   # Azure Speech Services
│       │   ├── testazure_mic_arabic.py        # Arabic microphone test
│       │   ├── testazure_mic_arabic_english.py # Bilingual test
│       │   └── credentials_template.md        # Credential template
│       └── google/                  # Google Speech Services
│           └── testgoogle.ipynb     # Google STT testing
│
├── 📚 documentation/                # Project Documentation
│   ├── technical_assessment/        # Assessment Documents
│   │   ├── Technical Assessment Omani Therapi.md     # Requirements
│   │   └── Technical Assessment_ OMANI-Therapist-Voice (2).pdf
│   ├── setup_guides/               # Setup Documentation
│   └── 7_12_2025_progress.md       # Development progress
│
├── 📊 data/                        # Data and Samples
│   ├── audio_samples/              # Audio Sample Files
│   │   └── omani_tts_samples/      # Omani TTS voice samples
│   └── session_transcripts/        # Session Data
│       ├── therapy_session_20250712_113157/  # Session recordings
│       └── therapy_session_20250712_114633/  # Session recordings
│
├── 🔧 tools/                       # Utility Tools
│   ├── security/                   # Security Tools
│   │   ├── security_check.py       # Security scanning script
│   │   └── GITHUB_UPLOAD_CHECKLIST.md  # Security checklist
│   └── testing/                    # Testing Tools
│
├── ⚙️ config/                      # Configuration Files
│   ├── environment/                # Environment Configuration
│   │   ├── env_template.txt        # Environment template
│   │   └── env_example.txt         # Environment examples
│   └── deployment/                 # Deployment Configuration
│       └── DEPLOYMENT_PLAN.md      # Deployment strategy
│
├── 🔒 .gitignore                   # Git ignore patterns
└── 📖 README.md                    # This file
```

## 🚀 Quick Start

### 1. Choose Your AI System

**Option A: Main System (OpenAI + Claude)**
```bash
cd ai_systems/main_system
pip install -r requirements.txt
python demo_ai_conversation.py
```

**Option B: Claude-Only System**
   ```bash
cd ai_systems/claude_only
pip install -r ../main_system/requirements.txt
python demo_claude_conversation.py
   ```

### 2. Configure Environment

   ```bash
# Copy environment template to project root
cp config/environment/env_template.txt .env

# Edit .env with your API keys
# AZURE_SPEECH_KEY=your_azure_key
# AZURE_SPEECH_REGION=your_region
# OPENAI_API_KEY=your_openai_key
# ANTHROPIC_API_KEY=your_anthropic_key
```

**Note:** The `.env` file should be in the project root directory so all systems can access it.

### 3. Test Speech Services

**Test Text-to-Speech:**
```bash
cd speech_services/text_to_speech
python test_azure_omani_tts.py
```

**Test Speech-to-Text:**
   ```bash
cd speech_services/speech_to_text/azure
python testazure_mic_arabic.py
```

## 🎯 Key Features

- **🗣️ Voice-Only Interface**: Complete hands-free interaction
- **⚡ Real-time Processing**: <20 second response latency
- **🇴🇲 Omani Arabic Support**: Native ar-OM language support
- **🧠 Dual AI Systems**: OpenAI GPT-4o + Claude Opus 4
- **🔄 Automatic Fallback**: Seamless API switching
- **🔒 Security First**: No hardcoded credentials
- **📊 Performance Monitoring**: Complete timing metrics

## 🛠️ Technical Stack

- **STT**: Azure Speech Services (ar-OM)
- **TTS**: Azure Speech Services (Omani voices)
- **AI Models**: OpenAI GPT-4o, Claude Opus 4, Claude 3.5 Sonnet
- **Audio**: 48kHz PCM, real-time processing
- **Languages**: Python 3.8+, PowerShell

## 📋 System Requirements

- Python 3.8 or higher
- Windows 10/11 (tested)
- Microphone and speakers
- Internet connection
- Azure Speech Services account
- OpenAI API key (for main system)
- Anthropic API key (for Claude systems)

## 🔧 Development

### Running Security Checks
```bash
cd tools/security
python security_check.py
```

### Testing Individual Components
```bash
# Test TTS only
cd speech_services/text_to_speech
python therapy_tts_example.py

# Test STT only
cd speech_services/speech_to_text/azure
python testazure_mic_arabic.py
```

## 📖 Documentation

- **Setup Guides**: `documentation/setup_guides/`
- **Technical Assessment**: `documentation/technical_assessment/`
- **Development Progress**: `documentation/7_12_2025_progress.md`
- **API Documentation**: Each system's README.md

## 🔒 Security

- All sensitive data removed from repository
- Environment variables for API keys
- Comprehensive `.gitignore` patterns
- Security scanning tools included

## 🤝 Contributing

1. Review the technical assessment in `documentation/technical_assessment/`
2. Check the development progress in `documentation/7_12_2025_progress.md`
3. Run security checks before commits: `tools/security/security_check.py`
4. Follow the folder structure for new additions

## 📞 Support

For technical issues or questions about the implementation, refer to:
- System-specific READMEs in each AI system folder
- Setup guides in `documentation/setup_guides/`
- Configuration examples in `config/environment/`

---

**Project Status**: ✅ Complete - Ready for deployment
**Last Updated**: January 12, 2025
**Version**: 1.0.0 

## v3_realtime_audio Branch

### Features
- **Realtime audio streaming**: Audio is streamed from the browser to the backend and TTS audio is streamed back in real time.
- **Strict turn-taking**: User cannot speak while the AI is talking. The microphone is disabled during TTS playback and re-enabled only after the AI response finishes.
- **No popups for audio**: TTS audio plays automatically in the browser without opening new tabs or popups.
- **All recent bug fixes and diagnostics**: Includes robust logging and diagnostics for both backend and frontend.

### Setup & Usage

1. **Clone the repository and checkout the branch:**
   ```sh
   git checkout v3_realtime_audio
   ```

2. **Backend setup:**
   - Install dependencies:
     ```sh
     cd fullstack_realtime/api
     pip install -r requirements.txt
     ```
   - Start the backend server:
     ```sh
     python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
     ```

3. **Frontend setup:**
   - Install dependencies:
     ```sh
     cd fullstack_realtime/frontend
     npm install
     ```
   - Start the frontend:
     ```sh
     npm start
     ```
   - Open your browser to [http://localhost:3000](http://localhost:3000)

### User Experience
- Speak into your microphone. The system will transcribe your speech, generate an AI response, and play the response as TTS audio.
- You cannot speak again until the AI's TTS response has finished playing.
- All audio is handled in the background—no popups or new tabs.
- Chat history is displayed in the UI for a natural conversation flow.

---

For more details, see the code and comments in the `v3_realtime_audio` branch. 