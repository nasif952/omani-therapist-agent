# Omani Therapist: Real-Time Voice-Only Omani Arabic Mental Health Chatbot

## Overview
Omani Therapist is a real-time, voice-only mental health chatbot designed for culturally sensitive, low-latency conversations in Omani Arabic. It leverages Azure Speech Services for speech-to-text (STT) and text-to-speech (TTS), and OpenAI GPT-4o (with Claude Opus 4 fallback) for AI-driven, empathetic responses. The system is built for turn-based, streaming audio interactions, ensuring a seamless, natural user experience.

## Features
- **Real-time, low-latency voice chat** (WebSocket streaming)
- **Omani Arabic support** (STT, TTS, and AI)
- **Strict turn-taking** (user cannot speak while TTS is playing)
- **Multi-turn conversations** in a single session
- **Frontend chat UI** with full message history
- **Cultural and clinical safety** (roadmap includes emotion detection, crisis intervention, HIPAA compliance)
- **Fallback to Claude Opus 4** if OpenAI GPT-4o is unavailable
- **Detailed logging** for debugging and research

## Architecture
```mermaid
graph TD
  A[User (Mic)] -- PCM Audio --> B(React Frontend)
  B -- WebSocket (PCM) --> C(Backend API)
  C -- Azure STT --> D[Transcription]
  C -- GPT-4o/Claude --> E[AI Response]
  C -- Azure TTS --> F[TTS Audio Chunks]
  C -- WebSocket (Base64 Audio) --> B
  B -- Audio Playback --> A
  B -- Chat UI --> G[Message History]
```

## Tech Stack
- **Frontend:** React, Web Audio API, WebSocket
- **Backend:** Python (FastAPI), Azure Speech Services, OpenAI GPT-4o, Claude Opus 4
- **Audio:** Raw PCM streaming, WAV conversion, base64 TTS
- **Deployment:** (see `config/deployment/`)

## Setup Instructions
### Prerequisites
- Python 3.10+
- Node.js 18+
- Azure Speech Services account
- OpenAI API key (GPT-4o)
- (Optional) Anthropic Claude API key

### Backend Setup
```bash
cd fullstack/api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
# Set environment variables (see config/environment/env_template.txt)
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd fullstack/frontend
npm install
npm start
```

### Environment Variables
- Copy `config/environment/env_template.txt` to `.env` and fill in your keys.

## Usage Guide
1. Start backend and frontend as above.
2. Open the frontend in your browser.
3. Press the mic button to speak. Your voice is streamed in real time.
4. Wait for the AI therapist to respond (TTS audio will play automatically).
5. Speak again when the mic is re-enabled.
6. View the full chat history in the UI.

## Development & Debugging
- Logs are written for every audio chunk, STT, TTS, and AI event.
- See `documentation/` for guides and technical assessment.
- See `PATH_UPDATES_SUMMARY.md` and `PROJECT_STRUCTURE_REORGANIZATION.md` for recent changes.

## Contribution
Pull requests are welcome! Please see `tools/security/GITHUB_UPLOAD_CHECKLIST.md` before submitting.

## License
[MIT License](LICENSE)

## FAQ
**Q: Why Omani Arabic?**  
A: The project is designed for local cultural and linguistic relevance.

**Q: Can I use a different TTS/STT provider?**  
A: The backend is modular; see `speech_services/` for alternatives.

**Q: How is user privacy handled?**  
A: No conversations are stored by default. See roadmap for HIPAA compliance.

## Troubleshooting
- **Audio not streaming?**  
  - Check browser permissions and backend logs.
- **TTS not playing?**  
  - Ensure audio chunks are received and base64 decoded in the frontend.
- **API keys not working?**  
  - Double-check your `.env` file and Azure/OpenAI dashboards.

---
For a detailed project history and technical log, see `PROJECT_HISTORY.md`. 