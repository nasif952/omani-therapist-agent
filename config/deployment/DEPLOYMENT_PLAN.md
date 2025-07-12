# GitHub Upload & Deployment Plan

## 🎯 Objective
Upload Omani Therapy Voice System to GitHub without API exposure + prepare for Vercel/Netlify deployment

---

## 📋 STEP-BY-STEP EXECUTION PLAN

### **PHASE 1: SECURITY & CODE CLEANUP** 🔒

#### **Step 1.1: Remove Hardcoded API Keys**
**Current Issue**: API keys hardcoded in multiple files
**Files to Clean**:
- `speech2texttest/azure/testazure_mic_arabic.py`
- `speech2texttest/azure/testazure_mic_arabic_english.py`
- `text2speech/test_azure_omani_tts.py`
- `text2speech/therapy_tts_example.py`

**Action**: Replace hardcoded keys with environment variable loading

#### **Step 1.2: Update .gitignore**
**Add to .gitignore**:
```
# Environment variables
.env
.env.local
.env.production
.env.development

# Azure credentials
azure_credentials.json
credentials.json

# Audio files (large)
*.wav
*.mp3
omani_tts_samples/
therapy_session_*/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

#### **Step 1.3: Create Environment Template**
**Create**: `.env.example`
```
# Azure Speech Services Configuration
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=uaenorth
AZURE_SPEECH_ENDPOINT=https://uaenorth.api.cognitive.microsoft.com/

# Optional: Backup key
AZURE_SPEECH_KEY_BACKUP=your_backup_key_here
```

---

### **PHASE 2: PROJECT STRUCTURE FOR DEPLOYMENT** 🏗️

#### **Step 2.1: Create Modular Architecture**
**New Structure**:
```
omani-therapy-voice/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── stt_service.py      # Speech-to-Text service
│   │   ├── tts_service.py      # Text-to-Speech service
│   │   └── config.py           # Configuration management
│   ├── therapy/
│   │   ├── __init__.py
│   │   ├── templates.py        # Therapy text templates
│   │   └── session_manager.py  # Session handling
│   └── utils/
│       ├── __init__.py
│       ├── audio_utils.py      # Audio processing utilities
│       └── error_handling.py   # Error handling
├── tests/
│   ├── test_stt.py
│   ├── test_tts.py
│   └── test_integration.py
├── docs/
│   ├── SETUP.md
│   ├── API_REFERENCE.md
│   └── DEPLOYMENT.md
├── scripts/
│   ├── test_stt.py            # STT testing script
│   ├── test_tts.py            # TTS testing script
│   └── interactive_demo.py    # Interactive testing
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── app.py                     # Flask/FastAPI entry point
```

#### **Step 2.2: Create Core Services**
**Modular Services**:
- `STTService`: Handles speech recognition
- `TTSService`: Handles speech synthesis
- `ConfigManager`: Manages environment variables
- `TherapyTemplates`: Manages therapy content

#### **Step 2.3: Create Flask App Structure**
**app.py** (ready for deployment):
```python
from flask import Flask, request, jsonify
from src.core.stt_service import STTService
from src.core.tts_service import TTSService
from src.core.config import ConfigManager

app = Flask(__name__)

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    # STT endpoint
    pass

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    # TTS endpoint
    pass

if __name__ == '__main__':
    app.run(debug=True)
```

---

### **PHASE 3: GITHUB PREPARATION** 📤

#### **Step 3.1: Create Professional README**
**Content**:
- Project overview
- Installation instructions
- Environment setup
- API usage examples
- Deployment guide

#### **Step 3.2: Create requirements.txt**
**Dependencies**:
```
azure-cognitiveservices-speech==1.34.0
python-dotenv==1.0.0
flask==2.3.3
pygame==2.5.2
requests==2.31.0
```

#### **Step 3.3: Create Setup Scripts**
**setup.sh** (for easy installation):
```bash
#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
echo "Setup complete! Edit .env with your Azure credentials."
```

---

### **PHASE 4: DEPLOYMENT READINESS** 🚀

#### **Step 4.1: Vercel Configuration**
**Create**: `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "AZURE_SPEECH_KEY": "@azure_speech_key",
    "AZURE_SPEECH_REGION": "@azure_speech_region"
  }
}
```

#### **Step 4.2: Environment Variable Management**
**Production Setup**:
- Vercel environment variables
- Local development with .env
- Docker support (optional)

#### **Step 4.3: API Documentation**
**Create**: API endpoints documentation for integration

---

## ✅ EXECUTION CHECKLIST

### **Security Checklist**:
- [ ] Remove all hardcoded API keys
- [ ] Update .gitignore to protect credentials
- [ ] Create .env.example template
- [ ] Verify no secrets in git history
- [ ] Test with environment variables

### **Code Structure Checklist**:
- [ ] Create modular service classes
- [ ] Implement proper error handling
- [ ] Add configuration management
- [ ] Create reusable components
- [ ] Add type hints and documentation

### **Deployment Checklist**:
- [ ] Create Flask app structure
- [ ] Set up requirements.txt
- [ ] Create Vercel configuration
- [ ] Test local development setup
- [ ] Verify environment variable loading

### **Documentation Checklist**:
- [ ] Professional README.md
- [ ] API documentation
- [ ] Setup instructions
- [ ] Deployment guide
- [ ] Troubleshooting guide

---

## 🚀 DEPLOYMENT TARGETS

### **Vercel (Recommended)**:
- **Pros**: Excellent Python support, easy environment variables, fast deployment
- **Setup**: `vercel.json` + environment variables
- **Cost**: Free tier available

### **Netlify**:
- **Pros**: Good for static sites, CI/CD integration
- **Setup**: `netlify.toml` + functions
- **Note**: Better for frontend, requires serverless functions for Python

### **Railway/Render (Alternative)**:
- **Pros**: Full backend support, database integration
- **Setup**: Direct Python deployment
- **Cost**: More expensive but more features

---

## 📊 TIMELINE

### **Day 1 (Today)**:
- [ ] Phase 1: Security cleanup (2 hours)
- [ ] Phase 2: Project restructure (3 hours)
- [ ] Phase 3: GitHub preparation (1 hour)

### **Day 2**:
- [ ] Phase 4: Deployment setup (2 hours)
- [ ] Testing and validation (2 hours)
- [ ] Documentation completion (1 hour)

### **Ready for GitHub**: End of Day 1
### **Ready for Deployment**: End of Day 2

---

## 🎯 SUCCESS CRITERIA

### **GitHub Ready**:
- ✅ No API keys exposed
- ✅ Professional project structure
- ✅ Complete documentation
- ✅ Easy setup process

### **Deployment Ready**:
- ✅ Flask app structure
- ✅ Environment variable management
- ✅ Vercel/Netlify configuration
- ✅ API endpoints functional

### **Production Quality**:
- ✅ Error handling
- ✅ Logging
- ✅ Rate limiting (future)
- ✅ Security headers (future)

---

*Ready to execute? Let's start with Phase 1!* 