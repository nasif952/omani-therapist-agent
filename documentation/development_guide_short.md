# 3-Day Development Guide: Completing Omani Therapist AI Technical Assessment

## Overview

With only 3 days remaining, this guide prioritizes essential tasks to deliver a functional voice-only Omani Arabic mental health chatbot meeting core requirements: <20s latency, dual-model AI, cultural sensitivity, and basic crisis protocols. Focus on wrapping the existing Python integration (omani_therapist_ai.py) into a web demo while ensuring minimal viability for all deliverables.

**Codebase Analysis:**
- Core integration complete: Python script with Azure STT, GPT-4o/Claude AI, Azure TTS, session memory, timing metrics
- Functional command-line demo exists
- Missing: Web interface, real-time streaming, full crisis protocols, documentation
- Security: Basic env vars; needs web security

**Daily Goals:** Create web wrapper for existing script, enhance with requirements, test thoroughly, prepare submission.

---

## Day 1: Web Wrapper & Real-Time Integration

**Objective:** Wrap existing Python script in web app with real-time voice.

1. **Set Up Web Framework (1-2 hours)**
   - Use React.js frontend + FastAPI backend (matches Python script)
   - Install: socket.io-client (front), fastapi, uvicorn, python-socketio (back)
   - Create components: VoiceRecordButton, ResponsePlayer, ChatHistory, LatencyDisplay

2. **Implement Real-Time Streaming (2-3 hours)**
   - Use FastAPI WebSockets for bidirectional audio
   - Frontend: MediaRecorder to stream chunks
   - Backend: Adapt omani_therapist_ai.py to process streamed audio
   - Handle partial recognition for continuous speech

3. **Integrate Existing Pipeline (2-3 hours)**
   - Wrap script functions in FastAPI endpoints/WebSockets
   - Stream: Client audio → STT → AI → TTS → Client playback
   - Add timing metrics to web display
   - Verify <20s latency in browser

4. **Basic Enhancements (1 hour)**
   - Add Omani prompts if not in script
   - Implement keyword-based crisis detection with alert

**End-of-Day Milestone:** Web app running script's conversation loop with browser audio.

---

## Day 2: Testing, Optimization & Safety Features

**Objective:** Optimize web performance, add safety, prepare demos.

1. **Latency & Performance Testing (2-3 hours)**
   - Test browser-to-browser latency (simulate with recordings)
   - Optimize: Async processing, smaller chunks, cache common responses
   - Target: <15s average; handle network variations

2. **Cultural & Safety Protocols (2-3 hours)**
   - Verify dual-model fallback in web context
   - Enhance crisis: Add UI alert, emergency contacts
   - Test Omani sensitivity: Sample responses for cultural fit
   - Add session logging (anonymized)

3. **Cross-Device Testing (1-2 hours)**
   - Test mobile/desktop browsers (Chrome, Safari, Firefox)
   - Verify mic permissions, audio quality
   - Add responsive UI

4. **Demo Preparation (1 hour)**
   - Create 5 scenarios with pre-recorded Arabic audio
   - Script demo flow showing key features

**End-of-Day Milestone:** Optimized web app with safety features, passing tests.

---

## Day 3: Documentation, Demo & Final Polish

**Objective:** Complete polish, create deliverables, deploy.

1. **UI Polish (1-2 hours)**
   - Add indicators, timer, emergency button, chat display
   - Implement session controls

2. **Demo Video (2-3 hours)**
   - Record 10-min video: Overview, live web demo, metrics

3. **Documentation (2-3 hours)**
   - Update README: Web setup, architecture
   - Create docs: Architecture, Evaluation, Cultural Guide, Safety, Benchmarks
   - Add logs/transcripts

4. **Final Testing & Deployment (1-2 hours)**
   - End-to-end tests
   - Deploy: Vercel (front), Render/Heroku (back)
   - Verify public access
   - Clean GitHub commit

**End-of-Day Milestone:** Submission-ready package.

---

## Risk Management & Contingencies

- **If web integration fails:** Fall back to script demo with screen recording
- **Latency issues:** Simplify pipeline, use pre-recorded TTS
- **Time crunch:** Prioritize web voice loop + demo video
- **API limits:** Use mock responses for testing

This refined plan leverages existing Python integration for quick web wrapping. 