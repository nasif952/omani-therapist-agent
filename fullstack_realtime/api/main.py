import os
import base64
import tempfile
import re
import time
import logging
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
from dotenv import load_dotenv
from omani_therapist_ai import OmaniTherapistAI, TimingMetrics
from pydub import AudioSegment
import asyncio
import azure.cognitiveservices.speech as speechsdk

# Load environment variables
load_dotenv(dotenv_path='../.env')
load_dotenv()

# Setup logger
logger = logging.getLogger(__name__)

app = FastAPI(title="Omani Therapist AI API", version="1.0.0")

# CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI system
try:
    therapist_ai = OmaniTherapistAI()
    print("✅ Omani Therapist AI initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize AI system: {e}")
    therapist_ai = None

# Enhanced crisis detection patterns with comprehensive Arabic and English keywords
CRISIS_PATTERNS = [
    # Suicide-related keywords
    r'\b(suicide|انتحار|اقتل نفسي|أريد أن أموت|أريد الموت|أفكر في الانتحار|أقتل روحي|أنهي حياتي)\b',
    r'\b(kill myself|end my life|take my own life|أخلص من الحياة|أتخلص من نفسي|أموت أحسن)\b',
    
    # Self-harm keywords
    r'\b(hurt myself|أؤذي نفسي|أضر نفسي|أجرح نفسي|أعذب نفسي|أقطع نفسي|أحرق نفسي)\b',
    r'\b(cut myself|burn myself|harm myself|أضرب نفسي|أعاقب نفسي|أدمر نفسي)\b',
    
    # Hopelessness and despair
    r'\b(end it all|أنهي كل شيء|لا أستطيع المتابعة|مافي أمل|مافي فايدة|تعبت من الحياة)\b',
    r'\b(no hope|hopeless|give up|أستسلم|ما عاد أقدر|خلاص انتهيت|مافي معنى للحياة)\b',
    r'\b(can\'t go on|can\'t take it|أبي أموت|أبي أخلص|تعبت من كل شي|ما عاد أتحمل)\b',
    
    # Immediate help requests
    r'\b(help me|ساعدني|أحتاج مساعدة عاجلة|أحتاج مساعدة فورية|أنقذوني|أدعموني)\b',
    r'\b(save me|rescue me|أنقذني|أحتاج أحد|أبي أحد يساعدني|أحتاج دعم نفسي)\b',
    
    # Crisis expressions in Omani dialect
    r'\b(ما عاد أقدر|خلاص تعبت|أبي أموت|أبي أخلص|تعبت من الدنيا|مافي فايدة مني)\b',
    r'\b(أحس أني عبء|أحس أني مافي داعي لوجودي|الناس أحسن بدوني|أنا مشكلة على الكل)\b',
    
    # Mental health crisis terms
    r'\b(mental breakdown|nervous breakdown|انهيار نفسي|انهيار عصبي|أنهار نفسياً)\b',
    r'\b(losing my mind|going crazy|أفقد عقلي|أصير مجنون|أحس أني أجن|عقلي راح)\b',
    
    # Substance abuse crisis
    r'\b(overdose|جرعة زائدة|أبي أخذ حبوب كثير|أشرب دوا كثير|أبي أسكر وأموت)\b',
    
    # Family/relationship crisis
    r'\b(أبي أهرب من البيت|أبي أترك كل شي|مافي أحد يحبني|كلهم يكرهونني)\b',
    r'\b(أحس أني وحيد|مافي أحد يفهمني|أحس أني منبوذ|أحس أني مرفوض)\b'
]

def detect_crisis(text: str) -> bool:
    """Basic crisis detection using regex patterns (expandable with ML)"""
    text_lower = text.lower()
    for pattern in CRISIS_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    return False

def enhance_ai_prompt_for_crisis(user_text: str, is_crisis: bool) -> str:
    """Enhanced AI prompt based on crisis detection with cultural sensitivity"""
    if is_crisis:
        crisis_guidance = """
        CRITICAL CRISIS RESPONSE PROTOCOL:
        
        The user has expressed thoughts or feelings that indicate they may be in serious psychological distress or crisis. 
        
        IMMEDIATE ACTIONS REQUIRED:
        1. **Validate and Empathize**: Acknowledge their pain without minimizing it
        2. **Cultural Sensitivity**: Respond in culturally appropriate Omani Arabic
        3. **Immediate Safety**: Ask if they are safe right now
        4. **Professional Help**: Strongly encourage immediate professional support
        5. **Local Resources**: Provide Omani crisis contacts:
           - Emergency: 999
           - Mental Health Support: Ministry of Health Psychological Support +968 24601999
           - Crisis Helpline: +968 80077000
        
        THERAPEUTIC APPROACH:
        - Use Islamic principles of hope and divine mercy ("رحمة الله واسعة")
        - Emphasize that seeking help is strength, not weakness
        - Remind them they are valued and their life has meaning
        - Avoid any statements that might increase guilt or shame
        
        SAFETY REMINDERS:
        - This is an AI, not a replacement for professional help
        - Encourage them to reach out to trusted family/friends
        - If immediate danger, suggest going to nearest hospital
        
        Respond with deep empathy, cultural understanding, and urgent care while maintaining professional boundaries.
        """
        return f"{crisis_guidance}\n\nUser message: {user_text}"
    return user_text

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "ai_system": "initialized" if therapist_ai else "failed",
        "timestamp": time.time()
    }

@app.post("/api/audio")
async def process_audio(file: UploadFile = File(...)):
    """Process audio input: STT -> AI -> TTS"""
    if not therapist_ai:
        raise HTTPException(status_code=500, detail="AI system not initialized")
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    ext = os.path.splitext(file.filename)[-1].lower()
    allowed_exts = ['.wav', '.webm', '.ogg', '.mp3', '.flac', '.m4a']
    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Unsupported audio format: {ext}")
    
    tmp_path = None
    wav_path = None
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Convert audio to a standard WAV format for robust processing by Azure.
        # This requires FFmpeg to be installed on the system.
        logger.info(f"Converting received audio file ({ext}) to WAV format...")
        audio_segment = AudioSegment.from_file(tmp_path)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_tmp:
            wav_path = wav_tmp.name
        
        # Export to 16kHz mono WAV, optimal for speech recognition
        audio_segment.export(wav_path, format="wav", parameters=["-ar", "16000", "-ac", "1"])
        logger.info(f"Successfully converted audio to WAV at: {wav_path}")
        
        # STT: Convert audio to text by passing the standardized WAV file path
        user_text, timing = therapist_ai.get_user_speech_from_file(wav_path)
        
    except Exception as e:
        logger.error(f"Failed to process audio file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Audio processing failed. Ensure FFmpeg is installed. Error: {str(e)}")
    finally:
        # Clean up temporary files
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        if wav_path and os.path.exists(wav_path):
            os.unlink(wav_path)
        
    if not user_text or not timing:
        return JSONResponse(
            status_code=200,
            content={"error": "No speech recognized. Please try speaking clearly."}
        )
    
    try:
        # Crisis detection (expandable)
        is_crisis = detect_crisis(user_text)
        enhanced_text = enhance_ai_prompt_for_crisis(user_text, is_crisis)
        
        # AI: Generate response
        ai_response = therapist_ai.get_ai_response(enhanced_text, timing)
        
        if not ai_response:
            return JSONResponse(
                status_code=200,
                content={"error": "AI failed to generate response. Please try again."}
            )
        
        # TTS: Convert response to speech
        tts_audio = therapist_ai.speak_text(ai_response, return_bytes=True)
        
        if not isinstance(tts_audio, (bytes, bytearray)):
            return JSONResponse(
                status_code=200,
                content={"error": "Speech synthesis failed. Please try again."}
            )
        
        # Encode audio as base64
        audio_b64 = base64.b64encode(tts_audio).decode('utf-8')
        
        return {
            "recognized_text": user_text,
            "ai_response": ai_response,
            "tts_audio_base64": audio_b64,
            "is_crisis_detected": is_crisis,
            "timing": timing.__dict__ if timing else None,
            "timestamp": time.time()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Processing failed: {str(e)}"}
        )

@app.post("/api/text")
async def process_text(text: str = Form(...)):
    """Process text input: Text -> AI -> TTS"""
    if not therapist_ai:
        raise HTTPException(status_code=500, detail="AI system not initialized")
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text provided")
    
    try:
        # Create dummy timing metrics
        now = time.time()
        timing = TimingMetrics(
            speech_start_time=now,
            speech_end_time=now,
            ai_processing_start_time=now,
            ai_processing_end_time=now,
            tts_start_time=now,
            tts_end_time=now,
            voice_playback_start_time=now
        )
        
        # Crisis detection
        is_crisis = detect_crisis(text)
        enhanced_text = enhance_ai_prompt_for_crisis(text, is_crisis)
        
        # AI: Generate response
        ai_response = therapist_ai.get_ai_response(enhanced_text, timing)
        
        if not ai_response:
            return JSONResponse(
                status_code=200,
                content={"error": "AI failed to generate response. Please try again."}
            )
        
        # TTS: Convert response to speech
        tts_audio = therapist_ai.speak_text(ai_response, return_bytes=True)
        
        if not isinstance(tts_audio, (bytes, bytearray)):
            return JSONResponse(
                status_code=200,
                content={"error": "Speech synthesis failed. Please try again."}
            )
        
        # Encode audio as base64
        audio_b64 = base64.b64encode(tts_audio).decode('utf-8')
        
        return {
            "user_text": text,
            "ai_response": ai_response,
            "tts_audio_base64": audio_b64,
            "is_crisis_detected": is_crisis,
            "timing": timing.__dict__,
            "timestamp": time.time()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Processing failed: {str(e)}"}
        )

@app.get("/api/session/transcript")
async def get_session_transcript():
    """Get current session transcript (expandable)"""
    if not therapist_ai:
        raise HTTPException(status_code=500, detail="AI system not initialized")
    
    try:
        # Save transcript and return path
        transcript_file = therapist_ai.save_session_transcript()
        
        if transcript_file:
            return {
                "transcript_file": transcript_file,
                "message_count": len(therapist_ai.session_memory),
                "timing_stats": therapist_ai.get_timing_statistics()
            }
        else:
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to save transcript"}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Transcript generation failed: {str(e)}"}
        )

@app.post("/api/session/reset")
async def reset_session():
    """Reset conversation session (expandable)"""
    if not therapist_ai:
        raise HTTPException(status_code=500, detail="AI system not initialized")
    
    try:
        therapist_ai.reset_session()
        return {
            "status": "session_reset",
            "timestamp": time.time()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Session reset failed: {str(e)}"}
        )

@app.websocket("/ws/audio")
async def websocket_audio_stream(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection accepted")
    
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION', 'uaenorth')
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = "ar-OM"
    
    # Configure for 16kHz mono PCM audio
    audio_format = speechsdk.audio.AudioStreamFormat(
        samples_per_second=16000,
        bits_per_sample=16,
        channels=1
    )
    
    stream = speechsdk.audio.PushAudioInputStream(stream_format=audio_format)
    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Use the main therapist_ai instance for AI and TTS
    global therapist_ai

    # State to store the last final transcript
    last_final_transcript = None

    async def recognize_loop():
        loop = asyncio.get_event_loop()
        # Remove the done event and its usage

        def recognized(evt):
            logger.info(f"Recognizer event: {evt.result.reason}, text: '{evt.result.text}'")
            nonlocal last_final_transcript
            if evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
                logger.info(f"Partial transcript: '{evt.result.text}'")
                asyncio.run_coroutine_threadsafe(
                    websocket.send_json({
                        "type": "partial_transcript",
                        "text": evt.result.text
                    }), loop)
            elif evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                last_final_transcript = evt.result.text
                logger.info(f"Final transcript: '{evt.result.text}'")
                asyncio.run_coroutine_threadsafe(
                    websocket.send_json({
                        "type": "final_transcript",
                        "text": evt.result.text
                    }), loop)
                # Do NOT set or wait for a done event

        def recognizing(evt):
            logger.info(f"Recognizing event: '{evt.result.text}'")

        def canceled(evt):
            logger.error(f"Recognizer canceled: {evt.reason}, details: {evt}")
            asyncio.run_coroutine_threadsafe(
                websocket.send_json({
                    "type": "error",
                    "text": f"Recognition canceled: {evt.reason}"
                }), loop)
            # Do NOT set or wait for a done event

        recognizer.recognizing.connect(recognizing)
        recognizer.recognized.connect(recognized)
        recognizer.canceled.connect(canceled)

        logger.info("Starting continuous recognition...")
        recognizer.start_continuous_recognition()
        # Do NOT await done.wait() or stop recognition here
        # Let the recognizer run until the websocket disconnects

    recog_task = asyncio.create_task(recognize_loop())

    try:
        while True:
            data = await websocket.receive_bytes()
            # logger.info(f"Received audio chunk of size {len(data)} bytes")
            stream.write(data)
            # logger.info("Wrote audio chunk to Azure stream")
            if last_final_transcript:
                logger.info(f"Final transcript detected: {last_final_transcript}")
                if therapist_ai is None:
                    logger.error("AI system not initialized")
                    last_final_transcript = None
                    continue
                logger.info("Calling AI for response...")
                ai_response = therapist_ai.get_ai_response(last_final_transcript, TimingMetrics(
                    speech_start_time=0, speech_end_time=0, ai_processing_start_time=0, ai_processing_end_time=0,
                    tts_start_time=0, tts_end_time=0, voice_playback_start_time=0
                ))
                logger.info(f"AI response received: {ai_response}")
                await websocket.send_json({"type": "ai_response", "text": ai_response})
                if ai_response:
                    logger.info("Starting TTS streaming...")
                    await websocket.send_json({"type": "tts_start"})
                    
                    # Use the therapist_ai instance to generate TTS audio
                    tts_audio_bytes = therapist_ai.speak_text(ai_response, return_bytes=True)
                    
                    if tts_audio_bytes and isinstance(tts_audio_bytes, bytes):
                        logger.info(f"TTS audio generated, size: {len(tts_audio_bytes)} bytes")
                        
                        # Stream the audio in chunks
                        chunk_size = 4096
                        chunk_count = 0
                        total_bytes = 0
                        
                        for i in range(0, len(tts_audio_bytes), chunk_size):
                            chunk = tts_audio_bytes[i:i + chunk_size]
                            chunk_count += 1
                            total_bytes += len(chunk)
                            logger.info(f"Sending TTS audio chunk #{chunk_count}, size {len(chunk)} bytes, total so far: {total_bytes}")
                            chunk_b64 = base64.b64encode(chunk).decode('utf-8')
                            await websocket.send_json({"type": "tts_audio", "chunk": chunk_b64})
                        
                        logger.info(f"TTS streaming complete: {chunk_count} chunks, {total_bytes} total bytes")
                    else:
                        logger.error(f"TTS audio generation failed: {type(tts_audio_bytes)}")
                    
                    await websocket.send_json({"type": "tts_end"})
                    logger.info("TTS streaming finished")
                last_final_transcript = None
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
        stream.close()
        recog_task.cancel()
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
        stream.close()
        recog_task.cancel()

# TODO: Expandable endpoints for future features
# @app.post("/api/emotional-analysis")  # For emotional state detection
# @app.get("/api/session/history")      # For conversation history UI
# @app.post("/api/crisis/escalate")     # For crisis escalation to professionals
# @app.get("/api/cultural/context")     # For cultural context adaptation

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 