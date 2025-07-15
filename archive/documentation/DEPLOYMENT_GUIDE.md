# 🚀 Omani Therapist AI - Deployment Guide

This guide covers deploying your Omani Therapist AI application using containerization. Since Vercel is **not suitable** for the Python backend due to system dependencies and execution limits, we recommend a split deployment strategy.

## 📋 Prerequisites

- Docker installed locally
- Git repository with your code
- API keys for Azure Speech, OpenAI, and Anthropic
- Domain name (optional)

## 🏗️ Architecture Overview

```
Frontend (React) ──────► Vercel/Netlify (Static Hosting)
     ↓
Backend (Python) ──────► Container Platform (Railway/Render/Cloud Run)
     ↓
External APIs ─────────► Azure Speech, OpenAI, Anthropic
```

## 🐳 Local Development with Docker

### 1. Environment Setup

Create a `.env` file in your project root:

```bash
# Azure Speech Services
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=uaenorth

# AI Services
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional: Database connections
# REDIS_URL=redis://localhost:6379
```

### 2. Build and Run Locally

```bash
# Build the Docker image
docker build -t omani-therapist-api .

# Run with Docker Compose (recommended)
docker-compose up -d

# Or run the container directly
docker run -p 8000:8000 --env-file .env omani-therapist-api
```

### 3. Test the API

```bash
# Health check
curl http://localhost:8000/api/health

# Test text endpoint
curl -X POST http://localhost:8000/api/text \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=مرحبا كيف حالك"
```

---

## 🌐 Production Deployment Options

### Option 1: Railway (Recommended for Startups)

**Pros:** Fast deployment, $5 free credits, real-time collaboration, usage-based billing
**Cons:** No traditional free tier after credits, manual background worker setup

#### Deployment Steps:

1. **Connect Repository:**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login and init project
   railway login
   railway init
   ```

2. **Deploy:**
   ```bash
   # Deploy your app
   railway up
   
   # Set environment variables
   railway variables set AZURE_SPEECH_KEY=your_key
   railway variables set AZURE_SPEECH_REGION=uaenorth
   railway variables set OPENAI_API_KEY=your_key
   railway variables set ANTHROPIC_API_KEY=your_key
   ```

3. **Custom Domain (Optional):**
   ```bash
   railway domain add your-domain.com
   ```

**Estimated Monthly Cost:** $10-20 for basic usage

---

### Option 2: Render (Recommended for Production)

**Pros:** Predictable pricing, always-on services, built-in background workers, excellent uptime
**Cons:** No free compute tier, per-user pricing for teams

#### Deployment Steps:

1. **Connect GitHub:** Go to [render.com](https://render.com) and connect your repository

2. **Use Blueprint:** The `render.yaml` file is already configured

3. **Set Environment Variables:** In Render dashboard:
   - `AZURE_SPEECH_KEY` → Your Azure key
   - `AZURE_SPEECH_REGION` → `uaenorth`
   - `OPENAI_API_KEY` → Your OpenAI key
   - `ANTHROPIC_API_KEY` → Your Anthropic key

4. **Deploy:** Render auto-deploys on Git pushes

**Estimated Monthly Cost:** $7-15 for starter plan

---

### Option 3: Google Cloud Run (Enterprise-Grade)

**Pros:** Excellent scaling, pay-per-use, serverless containers, Google's infrastructure
**Cons:** More complex setup, requires Google Cloud account

#### Deployment Steps:

1. **Setup Google Cloud:**
   ```bash
   # Install Google Cloud CLI
   # Enable Cloud Run API
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Build and Deploy:**
   ```bash
   # Build and push to Google Container Registry
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/omani-therapist-api
   
   # Deploy to Cloud Run
   gcloud run deploy omani-therapist-api \
     --image gcr.io/YOUR_PROJECT_ID/omani-therapist-api \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars AZURE_SPEECH_KEY=your_key,AZURE_SPEECH_REGION=uaenorth
   ```

**Estimated Monthly Cost:** $5-25 based on usage

---

### Option 4: Azure Container Instances (Synergy with Azure Speech)

Since you're already using Azure Speech Services, this provides excellent integration:

```bash
# Create resource group
az group create --name omani-therapist-rg --location eastus

# Create container instance
az container create \
  --resource-group omani-therapist-rg \
  --name omani-therapist-api \
  --image your-registry/omani-therapist-api:latest \
  --dns-name-label omani-therapist \
  --ports 8000 \
  --environment-variables \
    AZURE_SPEECH_KEY=your_key \
    AZURE_SPEECH_REGION=uaenorth
```

---

## 🎨 Frontend Deployment

Deploy your React frontend to Vercel (perfect for this):

### Vercel Deployment:

1. **Connect Repository:** Go to [vercel.com](https://vercel.com)

2. **Configure Build Settings:**
   ```bash
   # Build Command
   cd frontend && npm run build
   
   # Output Directory
   frontend/build
   ```

3. **Environment Variables:**
   ```bash
   REACT_APP_API_URL=https://your-api-domain.com
   ```

4. **Deploy:** Auto-deploys on Git pushes

---

## 🔧 Production Optimizations

### 1. Health Checks and Monitoring

All deployment configs include health checks at `/api/health`. Consider adding:

- **Uptime monitoring:** UptimeRobot, StatusCake
- **Error tracking:** Sentry
- **Performance monitoring:** DataDog, New Relic

### 2. Database Considerations

For production, consider managed databases:

- **PostgreSQL:** Supabase, PlanetScale, Railway Postgres
- **Redis:** Upstash, Redis Cloud
- **Vector Database:** Pinecone, Weaviate (for future AI features)

### 3. CDN and Static Assets

- **Images/Audio:** Cloudinary, AWS S3 + CloudFront
- **Frontend:** Automatic with Vercel/Netlify

### 4. Security Enhancements

```python
# Add to your FastAPI app
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["your-api-domain.com", "localhost"]
)
```

---

## 💰 Cost Comparison Summary

| Platform | Free Tier | Starter Cost | Best For |
|----------|-----------|--------------|----------|
| **Railway** | $5 credits (one-time) | $10/month | Fast prototyping, startups |
| **Render** | Static sites only | $7/month | Production apps, teams |
| **Google Cloud Run** | $0 + usage | $5-25/month | Enterprise, high-scale |
| **Azure Container** | $0 + usage | $10-30/month | Azure ecosystem |

---

## 🚨 Troubleshooting

### Common Issues:

1. **Audio dependencies failing:**
   ```bash
   # Add to Dockerfile if needed
   RUN apt-get install -y pulseaudio-utils
   ```

2. **Memory issues:**
   ```bash
   # Increase container memory limits
   # Railway: Upgrade plan
   # Render: Use Standard plan
   # Cloud Run: --memory 2Gi
   ```

3. **API timeout errors:**
   ```bash
   # Increase timeout in deployment configs
   # Add proper error handling for long AI responses
   ```

### Performance Tips:

- Use connection pooling for external APIs
- Implement response caching for repeated requests
- Add request queuing for high traffic
- Monitor CPU/memory usage and scale accordingly

---

## 🎯 Recommended Deployment Path

1. **Start with Railway** for development and testing ($5 free credits)
2. **Move to Render** for production deployment ($7/month predictable cost)
3. **Scale to Google Cloud Run** if you need enterprise features

This gives you the best balance of simplicity, cost, and scalability for your Omani Therapist AI application.

## 📞 Support

- **Railway:** [Discord](https://discord.gg/railway) 
- **Render:** [Community Forum](https://community.render.com/)
- **Google Cloud:** [Stack Overflow](https://stackoverflow.com/questions/tagged/google-cloud-run)

Happy deploying! 🚀 