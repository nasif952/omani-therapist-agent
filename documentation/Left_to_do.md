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
- Basic Omani Arabic TTS and STT integration
- OpenAI GPT-4o integration for AI responses
- **Dual-Model Strategy: Claude Opus 4 is already implemented as fallback to GPT-4o**

## 🛠️ How & Method
- WebSocket for low-latency audio streaming
- Azure Speech Services for STT and TTS
- OpenAI GPT-4o for AI responses
- Claude Opus 4 fallback for AI responses
- React (frontend), FastAPI (backend)
- State management with React hooks/refs
- Logging at every step for traceability

## ❓ Why
- Needed natural, real-time, voice-only chat for Omani Arabic mental health
- Previous REST/audio upload approach was slow and unreliable
- Turn-taking is essential for natural conversation
- Diagnostics/logs are critical for debugging and reliability

## 🚧 What Is Remaining (Prioritized by Technical Assessment)

### 🔴 HIGH PRIORITY - Core Technical Requirements
- **Dual-Model Evaluation & Reporting**: Validate, compare, and document the dual-model approach (OpenAI + Claude)
- **Intent Analysis & Emotional Detection**: Add emotional state detection and therapeutic context understanding
- **Cultural Adaptation**: Enhance Gulf-specific mental health terminology and cultural sensitivity
- **Performance Optimization**: Ensure <20 seconds end-to-end latency per conversation turn
- **Code-switching Support**: Handle Arabic-English mixing naturally
- **Crisis Intervention Protocols**: Implement suicide risk assessment and escalation
- **Safety Mechanisms**: Harmful content detection, professional referral triggers
- **HIPAA-compliant Data Handling**: Security implementation for clinical data

### 🟡 MEDIUM PRIORITY - Clinical & Safety Standards
- **Therapeutic Techniques**: Implement CBT techniques adaptation
- **Cultural Trauma-informed Approaches**: Add religious/spiritual integration
- **Session Recording Consent**: Data protection and anonymization protocols
- **Emergency Contact Integration**: Professional supervision pathways
- **Transparent AI Disclosure**: Clear user communication about AI nature

### 🟢 LOW PRIORITY - UI/UX & Documentation
- UI/UX polish (avatars, timestamps, mobile layout)
- Error handling (network, audio, backend failures)
- User settings (voice, speed, language, theme)
- Deployment scripts (Docker, CI/CD)
- Automated tests (unit, integration, e2e)
- Multi-user/session support
- Analytics and logging dashboard

## 📝 How Can Be Done

### Dual-Model Evaluation & Reporting
- Collect logs and results from both OpenAI and Claude responses
- Compare response quality, latency, and fallback frequency
- Write a model evaluation report (see Technical Assessment deliverables)
- Document the dual-model approach in architecture docs

### Intent Analysis & Emotional Detection
- Use Azure Cognitive Services for emotion detection
- Implement sentiment analysis on transcribed text
- Add therapeutic context classification (anxiety, depression, crisis, etc.)
- Store emotional state in conversation context

### Cultural Adaptation
- Enhance prompt engineering for Omani Arabic cultural context
- Add Gulf-specific mental health vocabulary
- Implement Islamic counseling integration
- Add cultural sensitivity filters and responses

### Crisis Intervention
- Implement suicide risk assessment algorithms
- Add escalation protocols with human intervention triggers
- Create emergency contact integration
- Add professional referral system

### Performance Optimization
- Implement response caching
- Optimize TTS chunking and streaming
- Add connection pooling and load balancing
- Monitor and log latency metrics

### Security & Compliance
- Implement data encryption at rest and in transit
- Add user consent management
- Implement data anonymization
- Add audit logging for HIPAA compliance

## 🔄 Alternatives
- Use Google or Amazon for STT/TTS (if Azure limits/costs)
- Use a state machine for turn-taking (XState, Redux)
- Use WebRTC for peer-to-peer audio (if scaling to 1:1 live)
- Use a queue/broker for TTS jobs (Celery, Redis)
- Use a monorepo tool (Nx, Turborepo) for better structure
- Use different emotion detection APIs (IBM Watson, Google Cloud)
- Use different crisis intervention frameworks

## 🤔 Why (Alternatives)
- Other cloud providers may offer better pricing or features
- State machines can make turn-taking logic more robust
- WebRTC is lower-latency for live calls, but more complex
- Queues help with scaling and reliability for TTS jobs
- Monorepo tools help with large, multi-team projects
- Different emotion APIs may have better Arabic language support
- Different crisis frameworks may be more culturally appropriate

## 📋 Required Deliverables (Technical Assessment)
1. **Working Voice Interface**: Deployed web application ✅ (partially done)
2. **Complete Source Code**: GitHub repository with full documentation ✅ (done)
3. **Architecture Documentation**: System design, data flow, model integration 🚧 (needs enhancement)
4. **Demo Video**: 10-minute conversation showcase 🚧 (needs creation)
5. **Model Evaluation Report**: Comparative analysis of dual-model approach 🚧 (needs implementation)
6. **Cultural Adaptation Guide**: Omani Arabic implementation details 🚧 (needs documentation)
7. **Safety Protocol Documentation**: Crisis intervention and escalation procedures 🚧 (needs implementation)
8. **Performance Benchmarks**: Latency, accuracy, and scalability metrics 🚧 (needs measurement)
9. **Test Conversation Logs**: 5+ different therapeutic scenarios 🚧 (needs creation)
10. **Deployment Instructions**: Production setup and maintenance guide 🚧 (needs enhancement)
11. **Future Roadmap**: Scaling and improvement recommendations ✅ (done)

## 🧪 Required Test Scenarios
- General anxiety consultation in Omani Arabic
- Family relationship counseling with cultural context
- Work stress management session
- Crisis intervention simulation (controlled environment)
- Code-switching conversation (Arabic-English mixing)

## ℹ️ Extra Info
- All major work is in `v3_realtime_audio` branch
- See `README.md` for setup and usage
- See `PATH_UPDATES_SUMMARY.md` for path/infra changes
- See daily logs in `documentation/7_13_2025.md`
- Technical Assessment timeline: 7 days
- Focus on clinical effectiveness and cultural competency

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
│   ├── technical_assessment/
│   │   └── Technical Assessment Omani Therapi.md
│   └── ...
├── ai_systems/
│   ├── main_system/
│   │   ├── omani_therapist_ai.py
│   │   ├── dual_model_strategy.py (NEW)
│   │   ├── emotional_detection.py (NEW)
│   │   ├── crisis_intervention.py (NEW)
│   │   └── ...
│   └── claude_only/
│       └── ...
├── fullstack_realtime/
│   ├── api/
│   │   ├── main.py
│   │   ├── safety_protocols.py (NEW)
│   │   ├── cultural_adaptation.py (NEW)
│   │   └── ...
│   └── frontend/
│       └── src/
│           ├── MicStreamTranscriber.tsx
│           ├── CrisisIntervention.tsx (NEW)
│           ├── CulturalContext.tsx (NEW)
│           └── ...
├── speech_services/
│   ├── text_to_speech/
│   └── speech_to_text/
├── config/
│   └── environment/
├── tests/
│   ├── therapeutic_scenarios/ (NEW)
│   ├── performance_benchmarks/ (NEW)
│   └── ...
└── tools/
    └── security/
```

--- 