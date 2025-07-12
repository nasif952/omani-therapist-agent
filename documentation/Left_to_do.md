# Left_to_do.md

## ✅ What Is Done
- Realtime audio streaming (STT and TTS) between frontend and backend
- Strict turn-taking: user cannot speak while TTS is playing
- No popups for audio: TTS plays in background
- Full chat UI with message history (alternating user/AI)
- Robust diagnostics/logging for TTS and WebSocket
- Bugfixes for TTS chunking, playback, and frontend/backend sync
- Documentation updated (README, PATH_UPDATES_SUMMARY.md)
- Branches: `fullstack_v2`, `v3_realtime_audio`

## 🛠️ How & Method
- WebSocket for low-latency audio streaming
- Azure Speech Services for STT and TTS
- OpenAI GPT-4o for AI responses
- React (frontend), FastAPI (backend)
- State management with React hooks/refs
- Logging at every step for traceability

## ❓ Why
- Needed natural, real-time, voice-only chat for Omani Arabic mental health
- Previous REST/audio upload approach was slow and unreliable
- Turn-taking is essential for natural conversation
- Diagnostics/logs are critical for debugging and reliability

## 🚧 What Is Remaining
- UI/UX polish (avatars, timestamps, mobile layout)
- Error handling (network, audio, backend failures)
- User settings (voice, speed, language, theme)
- Deployment scripts (Docker, CI/CD)
- Security review (CORS, auth, rate limiting)
- Automated tests (unit, integration, e2e)
- Multi-user/session support
- Analytics and logging dashboard
- Documentation for contributors

## 📝 How Can Be Done
- UI: CSS modules/styled-components, add avatars, timestamps, responsive design
- Error handling: try/catch, user notifications, fallback UI
- Settings: Modal/settings page, localStorage for preferences
- Deployment: Dockerfiles, GitHub Actions, deployment scripts
- Security: CORS config, JWT/auth, input validation, rate limiting middleware
- Tests: Jest/React Testing Library (frontend), pytest (backend), e2e with Playwright/Cypress
- Multi-user: Add session IDs, user auth, scalable backend
- Analytics: Integrate with logging/monitoring tools (e.g., Sentry, ELK)
- Docs: CONTRIBUTING.md, code comments, architecture diagrams

## 🔄 Alternatives
- Use Google or Amazon for STT/TTS (if Azure limits/costs)
- Use a state machine for turn-taking (XState, Redux)
- Use WebRTC for peer-to-peer audio (if scaling to 1:1 live)
- Use a queue/broker for TTS jobs (Celery, Redis)
- Use a monorepo tool (Nx, Turborepo) for better structure

## 🤔 Why (Alternatives)
- Other cloud providers may offer better pricing or features
- State machines can make turn-taking logic more robust
- WebRTC is lower-latency for live calls, but more complex
- Queues help with scaling and reliability for TTS jobs
- Monorepo tools help with large, multi-team projects

## ℹ️ Extra Info
- All major work is in `v3_realtime_audio` branch
- See `README.md` for setup and usage
- See `PATH_UPDATES_SUMMARY.md` for path/infra changes
- See daily logs in `documentation/7_13_2025.md`

## 🗂️ Probable Full Project Structure
```
main project/
├── .env
├── README.md
├── PATH_UPDATES_SUMMARY.md
├── documentation/
│   ├── 7_13_2025.md
│   ├── COMPREHENSIVE_DEVELOPMENT_GUIDE.md
│   ├── Left_to_do.md
│   └── ...
├── ai_systems/
│   ├── main_system/
│   │   ├── omani_therapist_ai.py
│   │   └── ...
│   └── claude_only/
│       └── ...
├── fullstack_realtime/
│   ├── api/
│   │   ├── main.py
│   │   └── ...
│   └── frontend/
│       └── src/
│           └── MicStreamTranscriber.tsx
├── speech_services/
│   ├── text_to_speech/
│   └── speech_to_text/
├── config/
│   └── environment/
└── tools/
    └── security/
```

--- 