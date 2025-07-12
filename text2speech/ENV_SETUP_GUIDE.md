# 🔐 Environment Variables Setup Guide

## ✅ **Why .env Files Are Better**

- **Easier**: No PowerShell commands to remember
- **Standard**: Industry-standard approach  
- **Secure**: Protected by `.gitignore`
- **Flexible**: Works for local development and deployment

## 🚀 **Quick Setup (30 seconds)**

### Step 1: Create Your .env File
```bash
# Copy the template (it already has your credentials!)
copy env_template.txt .env
```

### Step 2: Verify It Works  
```bash
# Check the file exists
dir .env

# Run the test
python test_azure_omani_tts.py
```

## 🔒 **Security: GitHub & Deployment**

### ✅ **Safe for GitHub:**
- The `.env` file is **automatically ignored** by Git
- Only `env_template.txt` gets uploaded (no real credentials)
- Your actual `.env` file stays on your local machine

### ✅ **Deployment (Production):**
When you deploy to a cloud service, you **don't use .env files**. Instead:

**Azure App Service:**
```bash
# Set environment variables in Azure portal
AZURE_SPEECH_KEY=your_key_here
AZURE_SPEECH_REGION=uaenorth
```

**Heroku:**
```bash
heroku config:set AZURE_SPEECH_KEY=your_key_here
heroku config:set AZURE_SPEECH_REGION=uaenorth
```

**Docker:**
```dockerfile
ENV AZURE_SPEECH_KEY=your_key_here
ENV AZURE_SPEECH_REGION=uaenorth
```

## 📁 **How It Works**

### **Local Development:**
1. You have `.env` file with real credentials
2. Python loads credentials from `.env` file
3. Git ignores `.env` file (never uploaded)

### **GitHub Repository:**
1. Only `env_template.txt` is uploaded (template)
2. Other developers copy template to create their own `.env`
3. No real credentials ever touch GitHub

### **Production Deployment:**
1. Set environment variables in hosting platform
2. Python reads from environment (not `.env` file)
3. Same code works everywhere

## 🔧 **File Structure**

```
text2speech/
├── env_template.txt       ✅ Safe for GitHub (template)
├── .env                   🔒 Your local credentials (ignored by Git)
├── .gitignore            ✅ Protects .env file
├── test_azure_omani_tts.py   ✅ Loads from .env automatically
└── therapy_tts_example.py    ✅ Loads from .env automatically
```

## 🆘 **Troubleshooting**

### **"Speech Key not found" Error**
```bash
# Make sure .env file exists
dir .env

# If missing, copy template
copy env_template.txt .env

# Check file content (should have your Azure keys)
type .env
```

### **"Module not found: dotenv" Error**
```bash
# Install the python-dotenv package
pip install python-dotenv

# Or install all requirements
pip install -r requirements.txt
```

### **Environment Variables Not Loading**
```bash
# Make sure .env file is in the same directory as the Python script
# Make sure there are no extra spaces around the = sign in .env
# Example correct format:
AZURE_SPEECH_KEY=your_key_here
# NOT: AZURE_SPEECH_KEY = your_key_here (spaces are bad)
```

## 🌟 **Benefits Over PowerShell Scripts**

| PowerShell Scripts | .env Files |
|-------------------|------------|
| ❌ Platform-specific | ✅ Works everywhere |
| ❌ Temporary variables | ✅ Persistent settings |
| ❌ Manual setup each time | ✅ One-time setup |
| ❌ Hard to remember commands | ✅ Simple file copy |
| ❌ Shell-dependent | ✅ Python-native |

## 🎉 **You're All Set!**

The `.env` approach is much simpler and more professional. Your credentials are secure, your code is clean, and everything works seamlessly from development to production. 