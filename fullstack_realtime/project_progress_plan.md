# Omani Therapist AI Full-Stack Project Progress Plan

This document outlines the sequential plan for building, testing, and deploying the full-stack application. It replicates the functionality of `omani_therapist_ai.py`, aligns with the technical assessment, incorporates research insights, and ensures expandability. The plan is divided into phases with tasks, dependencies, estimated time, and rationale.

## Overall Timeline & Assumptions
- **Total Time**: 3-5 hours (spread over sessions if needed), assuming API keys are ready.
- **Tools/Environment**: Python 3.10+, Node.js 18+, Git, Vercel account (free).
- **Project Root**: `omani_therapist_fullstack/` (new folder).
- **Expandability**: Each task includes notes for future extensions.
- **Testing**: Built-in at each phase.

## Phase 1: Project Setup (~15-20 min)
**Goal**: Create the base structure and copy core files.
1. Create root folder: Run `mkdir omani_therapist_fullstack`.
2. Create subfolders: `api/` (backend), `src/` (frontend React), `public/` (static assets).
3. Copy `omani_therapist_ai.py`: From `fullstack/` to `api/` (unchanged).
4. Add initial files:
   - `api/main.py` (FastAPI skeleton).
   - `api/requirements.txt` (minimal deps: fastapi, uvicorn, requests, python-dotenv).
   - `src/App.tsx` (React skeleton).
   - `package.json` (frontend deps: react, typescript).
   - `vercel.json` (deployment config).
   - `README.md` (basic instructions).
**Dependencies**: None.
**Rationale**: Starts with essentials; copying the script first ensures core logic is in place.
**Expandability Notes**: Structure allows adding modules easily (e.g., new API endpoints).

## Phase 2: Backend Development (~45-60 min)
**Goal**: Build the API layer around `omani_therapist_ai.py`.
5. Implement FastAPI in `api/main.py`:
   - Initialize app, CORS.
   - Endpoints: `/api/audio`, `/api/text`, `/api/health`.
   - Integrate copied script.
   - Add regex for exit/reset/crisis.
6. Add Azure REST Integration: Use `requests` for STT/TTS.
7. Environment Setup: Load `.env` vars.
8. Expandability: Add comments for future hooks.
**Dependencies**: Phase 1.
**Rationale**: Backend first, as it's the core. Keeps deps minimal.
**Expandability Notes**: Hooks for emotional analysis, advanced safety (e.g., ML-based crisis detection).

## Phase 3: Frontend Development (~45-60 min)
**Goal**: Build React UI connected to backend.
9. Scaffold React App: Use `npx create-react-app src --template typescript`.
10. Implement UI in `src/App.tsx`:
    - Voice recording, API calls, audio playback.
    - Status/error handling.
11. Add Proxy: In `package.json`, proxy to backend.
12. Expandability: Modular components.
**Dependencies**: Phase 2.
**Rationale**: Builds on backend; minimal/voice-focused.
**Expandability Notes**: Placeholders for chat history, crisis UI.

## Phase 4: Integration & Local Testing (~30-45 min)
**Goal**: Connect and test end-to-end.
13. Run Locally: Start backend, then frontend.
14. Test Scenarios: Anxiety consultation, crisis, reset, latency.
15. Fix Issues: Align mismatches.
16. Add Transcript Saving: Endpoint for logs.
**Dependencies**: Phases 2-3.
**Rationale**: Early testing prevents surprises.
**Expandability Notes**: Tests can be extended for new features.

## Phase 5: Deployment Preparation (~15-20 min)
**Goal**: Configure for Vercel.
17. Add `vercel.json`: Route API/static.
18. Git Init: Create repo, commit.
19. Env Vars: Document setup.
20. Expandability Docs: Update README.
**Dependencies**: Phase 4.
**Rationale**: Preps for seamless deploy.
**Expandability Notes**: Config supports scaling (e.g., add more routes).

## Phase 6: Deployment & Final Validation (~20-30 min)
**Goal**: Deploy and verify.
21. Push to GitHub: New repo.
22. Deploy on Vercel: Import, set env, deploy.
23. Live Testing: Voice flow on URL.
24. Backup: Azure if needed.
25. Demo Prep: Video instructions.
**Dependencies**: Phase 5.
**Rationale**: Ensures deployable version.
**Expandability Notes**: Deployed app can be updated easily.

## Execution Notes
- **Risks/Mitigations**: Fallback to SDK if REST latency high.
- **Your Input**: Pause/modify as needed. 