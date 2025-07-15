# 🚀 Deployment Guide - Omani Therapist AI

## Prerequisites

### System Requirements
- **Python**: 3.8+
- **Node.js**: 16+
- **Memory**: 4GB+ RAM
- **Storage**: 10GB+ free space

### API Keys Required
```bash
# OpenAI API
OPENAI_API_KEY=your_openai_key_here

# Anthropic Claude (Fallback)
ANTHROPIC_API_KEY=your_anthropic_key_here

# Azure Cognitive Services
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here
```

## Quick Start

### 1. Backend Setup
```bash
# Install dependencies
cd api
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key
export AZURE_SPEECH_KEY=your_key
export AZURE_SPEECH_REGION=your_region

# Start API server
python main.py
```

### 2. Frontend Setup
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
```

### 3. Access Application
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/api/health

## Docker Deployment

### Build and Run
```bash
# Build containers
docker-compose build

# Start services
docker-compose up -d
```

### Environment Configuration
```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - AZURE_SPEECH_KEY=${AZURE_SPEECH_KEY}
      - AZURE_SPEECH_REGION=${AZURE_SPEECH_REGION}
```

## Production Deployment

### Cloud Platform Options
1. **AWS**: ECS + ALB
2. **Azure**: Container Instances
3. **Google Cloud**: Cloud Run
4. **Digital Ocean**: App Platform

### Performance Optimization
- **Caching**: Redis for response caching
- **Load Balancing**: Multiple API instances
- **CDN**: Static file delivery
- **Database**: PostgreSQL for session management

## Monitoring & Health Checks

### Health Endpoints
- `/api/health` - System status
- `/api/metrics` - Performance metrics
- `/api/logs` - Error logging

### Monitoring Setup
```python
# Basic monitoring
import logging
logging.basicConfig(level=logging.INFO)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": time.time()}
```

## Security Configuration

### API Security
- **Rate Limiting**: 100 requests/minute
- **CORS**: Configured for frontend domain
- **Authentication**: API key validation
- **Encryption**: TLS/SSL for all traffic

### Data Protection
- **No Storage**: Voice data not persisted
- **Encryption**: In-transit encryption
- **Privacy**: No personal data retention
- **HIPAA**: Compliant data handling

## Troubleshooting

### Common Issues
1. **API Timeout**: Increase timeout to 60s
2. **Memory Issues**: Allocate 4GB+ RAM
3. **Voice Processing**: Check Azure Speech keys
4. **Model Errors**: Verify OpenAI API limits

### Debug Commands
```bash
# Check API health
curl http://localhost:8000/api/health

# Test text endpoint
curl -X POST http://localhost:8000/api/text -d "text=مرحبا"

# View logs
docker-compose logs -f api
```

## Scaling Guidelines

### Horizontal Scaling
- **API Instances**: 3-5 replicas
- **Load Balancer**: Round-robin distribution
- **Database**: Read replicas
- **Cache**: Distributed Redis

### Performance Tuning
- **Timeout**: 30-60 seconds
- **Concurrency**: 10-20 workers
- **Memory**: 2GB per instance
- **CPU**: 2 cores per instance

---

*Ready for production deployment* 