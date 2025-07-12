# 🇴🇲 Omani Therapist AI - Full-Stack Application

A voice-enabled mental health support chatbot that communicates exclusively in Omani Arabic dialect, providing culturally sensitive therapeutic conversations with real-time speech processing capabilities.

## 🎯 Project Overview

This full-stack application replicates and extends the functionality of `omani_therapist_ai.py` with:

- **Voice-Only Interaction**: Real-time audio recording, STT, AI response, and TTS playback
- **Cultural Sensitivity**: Omani Arabic dialect support with Islamic values integration
- **Crisis Detection**: Basic regex-based crisis detection with escalation prompts
- **Therapeutic Features**: Session memory, conversation history, transcript saving
- **Expandable Architecture**: Modular design for future enhancements

## 🏗️ Architecture

```
fullstack/
├── api/                          # Backend (Python + FastAPI)
│   ├── main.py                   # API endpoints and integration
│   ├── omani_therapist_ai.py     # Core AI logic (unchanged)
│   └── requirements.txt          # Python dependencies
├── frontend/                     # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── App.tsx              # Main application component
│   │   └── App.css              # Comprehensive styling
│   ├── package.json             # Node dependencies + proxy config
│   └── public/                  # Static assets
├── vercel.json                  # Deployment configuration
└── README.md                    # This file
```

## ✨ Features

### Core Functionality
- **🎤 Voice Recording**: WebM/Opus preferred, WAV fallback
- **🗣️ Speech-to-Text**: Azure Cognitive Services (Omani Arabic)
- **🤖 AI Response**: OpenAI GPT-4o primary, Claude fallback
- **🔊 Text-to-Speech**: Azure Neural Voices (Omani Arabic)
- **💬 Text Mode**: Alternative text input for accessibility

### Safety & Cultural Features
- **🚨 Crisis Detection**: Regex-based detection with professional referral prompts
- **🕌 Cultural Sensitivity**: Islamic values, family dynamics, social norms
- **📝 Session Management**: Memory, history, transcript saving
- **⏱️ Performance Timing**: <20s end-to-end latency tracking

### UI/UX Features
- **📱 Responsive Design**: Mobile-friendly, accessible interface
- **🎨 Cultural Colors**: Green-based theme respecting cultural preferences
- **♿ Accessibility**: Screen reader support, keyboard navigation
- **🌙 Crisis UI**: Special alerts and escalation guidance

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ with pip
- Node.js 18+ with npm
- API Keys (see Environment Setup)

### 1. Environment Setup
Create a `.env` file in the project root:
```env
# Azure Speech Services (REQUIRED)
AZURE_SPEECH_KEY=your_azure_key
AZURE_SPEECH_REGION=uaenorth

# OpenAI API (Primary AI)
OPENAI_API_KEY=your_openai_key

# Anthropic API (Fallback AI)
ANTHROPIC_API_KEY=your_anthropic_key

# Optional: Backup Azure key
AZURE_SPEECH_KEY_BACKUP=your_backup_key
```

### 2. Backend Setup
```bash
cd fullstack/api
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd fullstack/frontend
npm install
```

### 4. Local Development
**Terminal 1 (Backend):**
```bash
cd fullstack/api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd fullstack/frontend
npm start
```

Visit: http://localhost:3000

## 🌐 Deployment

### Deploy to Vercel (Recommended)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/omani-therapist-ai.git
   git push -u origin main
   ```

2. **Deploy on Vercel:**
   - Visit [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Set environment variables in Vercel dashboard
   - Deploy automatically

3. **Set Environment Variables in Vercel:**
   - Go to Project Settings → Environment Variables
   - Add all variables from your `.env` file

### Alternative: Azure App Service
If Vercel has limitations, deploy to Azure App Service:
```bash
# Install Azure CLI
az webapp create --resource-group myResourceGroup --plan myPlan --name omani-therapist-ai --runtime "PYTHON|3.9"
az webapp config appsettings set --resource-group myResourceGroup --name omani-therapist-ai --settings @env-vars.json
```

## 🧪 Testing Scenarios

### Required Demo Cases (from Technical Assessment):
1. **General Anxiety**: "أشعر بالقلق من العمل" (I feel anxious about work)
2. **Family Counseling**: "أواجه مشاكل مع عائلتي" (I'm having problems with my family)
3. **Work Stress**: "ضغط العمل يؤثر عليّ" (Work pressure is affecting me)
4. **Crisis Simulation**: "أحتاج مساعدة عاجلة" (I need urgent help)
5. **Code-switching**: Mix of Arabic and English

### Testing Commands:
- **Reset Session**: "بداية جديدة" or "reset"
- **Exit**: "انتهى" or "exit"
- **Crisis Keywords**: "انتحار", "ساعدني", "أؤذي نفسي"

## 🔧 API Endpoints

### Backend API (`/api/`)
- `GET /api/health` - Health check and system status
- `POST /api/audio` - Process audio input (STT → AI → TTS)
- `POST /api/text` - Process text input (Text → AI → TTS)
- `GET /api/session/transcript` - Download session transcript
- `POST /api/session/reset` - Reset conversation session

### Response Format:
```json
{
  "recognized_text": "User's speech as text",
  "ai_response": "AI therapist response",
  "tts_audio_base64": "Base64 encoded audio",
  "is_crisis_detected": false,
  "timing": {...},
  "timestamp": 1234567890
}
```

## 🔮 Expandability

### Backend Extensions (TODO comments in code):
```python
# Emotional Analysis
@app.post("/api/emotional-analysis")
async def analyze_emotion(text: str):
    # Add ML-based emotion detection
    pass

# Advanced Crisis Detection
@app.post("/api/crisis/escalate")
async def escalate_crisis(session_id: str):
    # Connect to professional services
    pass

# Cultural Context Adaptation
@app.get("/api/cultural/context")
async def get_cultural_context():
    # Dynamic cultural adaptation
    pass
```

### Frontend Extensions:
- **Session History UI**: Persistent conversation logs
- **Voice Settings**: Voice gender, speed, emotion controls
- **Crisis Resources**: Local helpline integration
- **Multi-language**: Expand beyond Omani Arabic
- **Professional Dashboard**: For therapist oversight

### Infrastructure Extensions:
- **Database Integration**: PostgreSQL for session persistence
- **Authentication**: User accounts and privacy
- **Analytics**: Usage patterns and effectiveness metrics
- **Mobile App**: React Native version

## 🛠️ Troubleshooting

### Common Issues:

**Backend won't start:**
```bash
# Check Python version
python --version  # Should be 3.9+

# Install missing dependencies
pip install -r api/requirements.txt

# Check environment variables
python -c "import os; print(os.getenv('AZURE_SPEECH_KEY'))"
```

**Frontend can't connect to backend:**
```bash
# Verify proxy in package.json
grep -A1 "proxy" frontend/package.json

# Check backend is running
curl http://localhost:8000/api/health
```

**Audio recording not working:**
- Check browser permissions (Chrome: Settings → Privacy → Microphone)
- Use HTTPS in production (microphone requires secure context)
- Test with different browsers

**Azure Speech errors:**
- Verify API key and region in `.env`
- Check Azure quota limits
- Test with smaller audio files

**Deployment issues:**
- Ensure all environment variables are set in Vercel
- Check build logs for missing dependencies
- Verify Python runtime version in vercel.json

### Performance Optimization:
- **Latency**: Monitor timing metrics in API responses
- **Audio Quality**: Use WebM/Opus for smaller file sizes
- **Caching**: Implement Redis for session storage
- **CDN**: Use Vercel's edge network for global distribution

## 📊 Monitoring

### Key Metrics to Track:
- **Response Latency**: Target <20s per conversation turn
- **Crisis Detection Rate**: Monitor false positives/negatives
- **User Engagement**: Session length, return visits
- **Cultural Appropriateness**: User feedback on responses

### Logging:
```python
# Backend automatically logs:
- STT processing time
- AI response generation time
- TTS synthesis time
- Crisis detection events
- Error rates and types
```

## 🤝 Contributing

### Development Workflow:
1. Create feature branch
2. Implement changes with tests
3. Update documentation
4. Submit pull request

### Code Standards:
- **Backend**: Follow PEP 8, type hints, docstrings
- **Frontend**: ESLint + Prettier, TypeScript strict mode
- **Accessibility**: WCAG 2.1 AA compliance
- **Cultural Sensitivity**: Native speaker review required

## 📄 License & Ethics

### Important Notes:
- **Not Medical Advice**: This is an AI assistant, not professional therapy
- **Privacy**: Sessions are not stored permanently (configurable)
- **Cultural Respect**: Designed with Omani cultural consultation
- **Crisis Protocol**: Always directs to professional help when needed

### Compliance:
- GDPR compliant (EU users)
- HIPAA considerations (healthcare data)
- UAE data protection laws
- Ethical AI guidelines

## 📞 Support

For technical issues or feature requests:
- Create GitHub issue with detailed description
- Include error logs and environment details
- Specify browser/device for frontend issues

---

**🇴🇲 Built with cultural sensitivity and therapeutic care for the Omani community** 