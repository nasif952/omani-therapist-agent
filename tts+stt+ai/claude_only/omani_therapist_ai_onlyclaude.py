#!/usr/bin/env python3
"""
Omani Therapist AI - Claude Opus 4 Only Version
===============================================

This system integrates:
- Speech-to-Text (STT) for Arabic speech recognition
- Claude Opus 4 (claude-opus-4-20250514) for therapeutic conversations
- Text-to-Speech (TTS) for natural Omani Arabic responses
- Session memory management
- Culturally-sensitive therapeutic conversations
- Performance timing measurements

Author: AI Assistant
Created: 2024
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import io

# Azure Speech Services
import azure.cognitiveservices.speech as speechsdk

# AI Services - Claude Only
try:
    import anthropic
except ImportError:
    anthropic = None

# Audio playback
import pygame

# Environment variables
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ConversationMessage:
    """Represents a single conversation message"""
    role: str  # 'user' or 'assistant' or 'system'
    content: str
    timestamp: datetime
    voice_gender: Optional[str] = None
    emotion: Optional[str] = None


@dataclass
class TimingMetrics:
    """Represents timing metrics for a conversation turn"""
    speech_start_time: float
    speech_end_time: float
    ai_processing_start_time: float
    ai_processing_end_time: float
    tts_start_time: float
    tts_end_time: float
    voice_playback_start_time: float
    
    @property
    def total_latency(self) -> float:
        """Total time from speech start to voice playback start"""
        return self.voice_playback_start_time - self.speech_start_time
    
    @property
    def stt_duration(self) -> float:
        """Time taken for speech-to-text"""
        return self.speech_end_time - self.speech_start_time
    
    @property
    def ai_processing_duration(self) -> float:
        """Time taken for AI processing"""
        return self.ai_processing_end_time - self.ai_processing_start_time
    
    @property
    def tts_duration(self) -> float:
        """Time taken for text-to-speech synthesis"""
        return self.tts_end_time - self.tts_start_time
    
    def print_timing_report(self):
        """Print detailed timing report"""
        print("\n" + "=" * 50)
        print("⏱️  TIMING PERFORMANCE REPORT (Claude Opus 4)")
        print("=" * 50)
        print(f"🎤 Speech Recognition: {self.stt_duration:.2f}s")
        print(f"🤖 Claude Processing:  {self.ai_processing_duration:.2f}s")
        print(f"🔊 TTS Synthesis:     {self.tts_duration:.2f}s")
        print(f"📊 TOTAL LATENCY:     {self.total_latency:.2f}s")
        print("=" * 50)


class OmaniTherapistAI_OnlyClaude:
    """
    Main conversation agent that integrates STT, Claude Opus 4, and TTS
    for therapeutic conversations in Omani Arabic with performance timing
    """
    
    def __init__(self):
        """Initialize the Omani Therapist AI system with Claude Opus 4 only"""
        # Load API keys from environment
        self.azure_speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.azure_region = os.getenv('AZURE_SPEECH_REGION', 'uaenorth')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Try backup Azure key if primary not found
        if not self.azure_speech_key:
            self.azure_speech_key = os.getenv('AZURE_SPEECH_KEY_BACKUP')
        
        # Validate required credentials
        if not self.azure_speech_key:
            raise ValueError("Azure Speech Key not found. Please set AZURE_SPEECH_KEY in environment variables.")
        
        if not self.anthropic_api_key:
            raise ValueError("Anthropic API key not found. Please set ANTHROPIC_API_KEY in environment variables.")
        
        # Initialize Claude client
        if not anthropic:
            raise ImportError("Anthropic library not found. Please install with: pip install anthropic")
        
        try:
            # Initialize Anthropic client for Claude Opus 4
            self.claude_client = anthropic.Anthropic(
                api_key=self.anthropic_api_key
            )
            logger.info("Claude Opus 4 client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Claude client: {e}")
            raise
        
        # Initialize Azure Speech services
        self._setup_azure_speech()
        
        # Initialize pygame for audio playback
        pygame.mixer.init(frequency=48000, size=-16, channels=1, buffer=1024)
        
        # Session memory (list of ConversationMessage objects)
        self.session_memory: List[ConversationMessage] = []
        self.max_memory_turns = 10  # Keep last 10 exchanges
        
        # Timing metrics storage
        self.timing_history: List[TimingMetrics] = []
        
        # Therapeutic system prompt for Claude Opus 4
        self.system_prompt = """أنت طبيب نفسي عماني مختص ومتفهم ومتطور. تجيب دائماً باللغة العربية العمانية، وتستخدم لغة حساسة ثقافياً ومراعية للأسرة والإيمان، والاستشارة العلاجية المتقدمة. إذا ذكر المستخدم ضائقة شديدة، شجعه دائماً على طلب المساعدة من شخص حقيقي أو خط المساعدة المحلي.

كن:
- متعاطف ومتفهم بعمق
- محترم للثقافة العمانية والإسلامية
- مهني في التعامل مع القضايا النفسية المعقدة
- مشجع ومحفز بطريقة إيجابية ومبتكرة
- حريص على توجيه المستخدم للمساعدة المهنية عند الحاجة
- قادر على فهم التفاصيل الدقيقة والمشاعر المعقدة

استخدم العبارات العمانية الأصيلة واللهجة المحلية عند المناسب. اعتمد على أحدث الممارسات في العلاج النفسي مع احترام التقاليد الثقافية العمانية."""
        
        # Add system message to memory
        self.session_memory.append(ConversationMessage(
            role="system",
            content=self.system_prompt,
            timestamp=datetime.now()
        ))
        
        # Available voices
        self.voices = {
            'male': 'ar-OM-AbdullahNeural',
            'female': 'ar-OM-AyshaNeural'
        }
        
        # Default settings
        self.default_voice_gender = "female"
        self.default_emotion = "neutral"
        
        logger.info("Omani Therapist AI (Claude Opus 4 Only) initialized successfully")
    
    def _setup_azure_speech(self):
        """Setup Azure Speech Services for STT and TTS"""
        try:
            # STT Configuration
            self.stt_config = speechsdk.SpeechConfig(
                subscription=self.azure_speech_key,
                region=self.azure_region
            )
            self.stt_config.speech_recognition_language = "ar-OM"  # Omani Arabic
            
            # TTS Configuration
            self.tts_config = speechsdk.SpeechConfig(
                subscription=self.azure_speech_key,
                region=self.azure_region
            )
            # Set HIGHEST quality audio format (48kHz uncompressed)
            self.tts_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm
            )
            
            logger.info(f"Azure Speech Services configured - Region: {self.azure_region}")
            
        except Exception as e:
            logger.error(f"Failed to setup Azure Speech Services: {e}")
            raise
    
    def get_user_speech(self, timeout_seconds: int = 10) -> Tuple[Optional[str], Optional[TimingMetrics]]:
        """
        Capture user speech using microphone and convert to text
        
        Args:
            timeout_seconds: Maximum time to wait for speech
            
        Returns:
            Tuple of (recognized text or None, timing metrics or None)
        """
        try:
            # Record speech start time
            speech_start_time = time.time()
            
            # Use default microphone
            audio_config = speechsdk.AudioConfig(use_default_microphone=True)
            
            # Create speech recognizer
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.stt_config,
                audio_config=audio_config
            )
            
            logger.info("🎤 Listening for speech...")
            print("🎤 Listening... (speak in Arabic)")
            
            # Recognize speech
            result = recognizer.recognize_once_async().get()
            
            # Record speech end time
            speech_end_time = time.time()
            
            if result and result.reason == speechsdk.ResultReason.RecognizedSpeech:
                user_text = result.text.strip()
                logger.info(f"✅ Recognized: {user_text}")
                
                # Create partial timing metrics (will be completed later)
                timing_metrics = TimingMetrics(
                    speech_start_time=speech_start_time,
                    speech_end_time=speech_end_time,
                    ai_processing_start_time=0,
                    ai_processing_end_time=0,
                    tts_start_time=0,
                    tts_end_time=0,
                    voice_playback_start_time=0
                )
                
                return user_text, timing_metrics
                
            elif result and result.reason == speechsdk.ResultReason.NoMatch:
                logger.warning("❌ No speech could be recognized")
                print("❌ No speech detected. Try speaking louder or closer to the microphone.")
                return None, None
                
            elif result and result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                logger.error(f"Speech recognition canceled: {cancellation_details.reason}")
                
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"Error details: {cancellation_details.error_details}")
                    if "401" in str(cancellation_details.error_details):
                        print("🚨 Authentication error - please check Azure credentials")
                    elif "microphone" in str(cancellation_details.error_details).lower():
                        print("🚨 Microphone permission issue - check Windows settings")
                
                return None, None
                
            else:
                logger.warning(f"Unexpected result: {result.reason if result else 'None'}")
                return None, None
                
        except Exception as e:
            logger.error(f"STT Exception: {e}")
            print(f"🚨 Speech recognition error: {e}")
            return None, None
    
    def _prepare_messages_for_claude(self) -> Tuple[str, List[Dict[str, str]]]:
        """
        Prepare recent conversation history for Claude API call
        
        Returns:
            Tuple of (system message, conversation messages)
        """
        # Get recent messages (last N turns)
        recent_messages = self.session_memory[-self.max_memory_turns:]
        
        # Separate system message from conversation
        system_message = ""
        conversation_messages = []
        
        for msg in recent_messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                conversation_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        return system_message, conversation_messages
    
    def _call_claude_opus4(self, system_message: str, messages: List[Dict[str, str]]) -> Optional[str]:
        """
        Call Claude Opus 4 API
        
        Args:
            system_message: System prompt
            messages: List of conversation messages
            
        Returns:
            AI response or None if failed
        """
        try:
            logger.info("🤖 Calling Claude Opus 4...")
            
            # Create Claude message with Opus 4 model (fallback to Sonnet if Opus 4 not available)
            try:
                response = self.claude_client.messages.create(
                    model="claude-opus-4-20250514",  # Latest Claude Opus 4 model
                    max_tokens=600,
                    temperature=0.7,
                    system=system_message,
                    messages=messages
                )
            except Exception as opus_error:
                logger.warning(f"Claude Opus 4 not available, falling back to Claude 3.5 Sonnet: {opus_error}")
                response = self.claude_client.messages.create(
                    model="claude-3-5-sonnet-20241022",  # Fallback to Claude 3.5 Sonnet
                    max_tokens=600,
                    temperature=0.7,
                    system=system_message,
                    messages=messages
                )
            
            # Extract text from response - handle both TextBlock and ToolUseBlock
            if response.content and len(response.content) > 0:
                content_block = response.content[0]
                if hasattr(content_block, 'text'):
                    ai_response = content_block.text.strip()
                    logger.info("✅ Claude Opus 4 response received")
                    return ai_response
                else:
                    logger.error(f"Claude response content type not supported: {type(content_block)}")
                    return None
            else:
                logger.error("Claude response has no content")
                return None
            
        except Exception as e:
            logger.error(f"Claude Opus 4 API error: {e}")
            return None
    
    def get_ai_response(self, user_input: str, timing_metrics: TimingMetrics) -> Optional[str]:
        """
        Get AI response using Claude Opus 4 only
        
        Args:
            user_input: User's input text
            timing_metrics: Timing metrics object to update
            
        Returns:
            AI response or None if failed
        """
        # Record AI processing start time
        timing_metrics.ai_processing_start_time = time.time()
        
        # Add user message to session memory
        self.session_memory.append(ConversationMessage(
            role="user",
            content=user_input,
            timestamp=datetime.now()
        ))
        
        # Prepare messages for Claude
        system_message, conversation_messages = self._prepare_messages_for_claude()
        
        # Call Claude Opus 4
        ai_response = self._call_claude_opus4(system_message, conversation_messages)
        
        # Record AI processing end time
        timing_metrics.ai_processing_end_time = time.time()
        
        # If we got a response, add it to memory
        if ai_response:
            self.session_memory.append(ConversationMessage(
                role="assistant",
                content=ai_response,
                timestamp=datetime.now(),
                voice_gender=self.default_voice_gender,
                emotion=self.default_emotion
            ))
        else:
            logger.error("❌ Claude Opus 4 failed to generate response")
        
        return ai_response
    

    def speak_text(self, text: str, voice_gender: str = "female", 
                   emotion: str = "neutral", timing_metrics: Optional[TimingMetrics] = None) -> bool:
        """
        Convert text to speech and play it
        
        Args:
            text: Arabic text to synthesize
            voice_gender: 'male' or 'female'
            emotion: 'calm', 'encouraging', 'excited', 'sad', 'neutral'
            timing_metrics: Optional timing metrics object to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Record TTS start time
            if timing_metrics:
                timing_metrics.tts_start_time = time.time()
            
            voice_name = self.voices.get(voice_gender, self.voices['female'])
            self.tts_config.speech_synthesis_voice_name = voice_name
            
            # Use simple text synthesis instead of SSML to avoid timeout issues
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.tts_config,
                audio_config=None
            )
            
            logger.info(f"🔊 Speaking: {text[:50]}...")
            print(f"🔊 Speaking: {text[:50]}...")
            
            # Use simple text synthesis which is faster and more reliable
            result = synthesizer.speak_text_async(text).get()
            
            # Record TTS end time
            if timing_metrics:
                timing_metrics.tts_end_time = time.time()
            
            if result and result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                if result.audio_data:
                    # Record voice playback start time
                    if timing_metrics:
                        timing_metrics.voice_playback_start_time = time.time()
                    
                    # Play audio using pygame
                    audio_stream = io.BytesIO(result.audio_data)
                    pygame.mixer.music.load(audio_stream)
                    pygame.mixer.music.play()
                    
                    # Wait for playback to complete
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
                
                logger.info("✅ Speech synthesis completed")
                return True
            elif result and result.reason == speechsdk.ResultReason.Canceled:
                # Handle TTS cancellation with detailed error information
                cancellation_details = result.cancellation_details
                logger.error(f"TTS Canceled: {cancellation_details.reason}")
                
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"TTS Error details: {cancellation_details.error_details}")
                    
                    # Check for specific error types
                    error_details = str(cancellation_details.error_details).lower()
                    
                    if "401" in error_details or "unauthorized" in error_details:
                        print("🚨 TTS Authentication Error:")
                        print("   - Check your AZURE_SPEECH_KEY in .env file")
                        print("   - Verify the key is valid and not expired")
                        print("   - Ensure the region is correct (uaenorth)")
                    elif "403" in error_details or "forbidden" in error_details:
                        print("🚨 TTS Permission Error:")
                        print("   - Your Azure subscription may not support this region")
                        print("   - Try changing AZURE_SPEECH_REGION to 'eastus' or 'westus2'")
                    elif "timeout" in error_details or "network" in error_details:
                        print("🚨 TTS Network Error:")
                        print("   - Check your internet connection")
                        print("   - Try again in a few moments")
                    elif "voice" in error_details or "neural" in error_details:
                        print("🚨 TTS Voice Error:")
                        print("   - The Omani voice may not be available in your region")
                        print("   - Try using a different voice or region")
                    else:
                        print(f"🚨 TTS Error: {cancellation_details.error_details}")
                        print("   - Check Azure Speech Service status")
                        print("   - Verify your subscription is active")
                
                return False
            else:
                logger.error(f"TTS Error: {result.reason if result else 'Unknown error'}")
                print(f"🚨 TTS failed with reason: {result.reason if result else 'Unknown'}")
                return False
                
        except Exception as e:
            logger.error(f"TTS Exception: {e}")
            print(f"🚨 Speech synthesis error: {e}")
            return False
    
    def get_timing_statistics(self) -> Dict[str, float]:
        """
        Get timing statistics from all recorded conversations
        
        Returns:
            Dictionary with timing statistics
        """
        if not self.timing_history:
            return {}
        
        total_latencies = [t.total_latency for t in self.timing_history]
        stt_durations = [t.stt_duration for t in self.timing_history]
        ai_durations = [t.ai_processing_duration for t in self.timing_history]
        tts_durations = [t.tts_duration for t in self.timing_history]
        
        return {
            'total_conversations': len(self.timing_history),
            'avg_total_latency': sum(total_latencies) / len(total_latencies),
            'min_total_latency': min(total_latencies),
            'max_total_latency': max(total_latencies),
            'avg_stt_duration': sum(stt_durations) / len(stt_durations),
            'avg_claude_duration': sum(ai_durations) / len(ai_durations),
            'avg_tts_duration': sum(tts_durations) / len(tts_durations)
        }
    
    def print_timing_statistics(self):
        """Print comprehensive timing statistics"""
        stats = self.get_timing_statistics()
        
        if not stats:
            print("📊 No timing data available yet")
            return
        
        print("\n" + "=" * 60)
        print("📊 CLAUDE OPUS 4 CONVERSATION TIMING STATISTICS")
        print("=" * 60)
        print(f"Total Conversations: {stats['total_conversations']}")
        print(f"Average Total Latency: {stats['avg_total_latency']:.2f}s")
        print(f"Best Response Time: {stats['min_total_latency']:.2f}s")
        print(f"Worst Response Time: {stats['max_total_latency']:.2f}s")
        print("-" * 60)
        print("BREAKDOWN BY COMPONENT:")
        print(f"  🎤 Speech Recognition: {stats['avg_stt_duration']:.2f}s avg")
        print(f"  🤖 Claude Opus 4:     {stats['avg_claude_duration']:.2f}s avg")
        print(f"  🔊 TTS Synthesis:      {stats['avg_tts_duration']:.2f}s avg")
        print("=" * 60)
    
    def save_session_transcript(self, filename: Optional[str] = None) -> str:
        """
        Save conversation transcript to file with timing data
        
        Args:
            filename: Optional filename, defaults to timestamp-based name
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"therapy_session_claude_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Omani Therapist AI - Claude Opus 4 Session Transcript\n")
                f.write("=" * 60 + "\n")
                f.write(f"Session Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"AI Model: Claude Opus 4 (claude-opus-4-20250514)\n")
                f.write(f"Total Messages: {len(self.session_memory)}\n")
                f.write("=" * 60 + "\n\n")
                
                for i, msg in enumerate(self.session_memory, 1):
                    if msg.role != "system":  # Skip system message in transcript
                        f.write(f"[{i}] {msg.role.upper()} ({msg.timestamp.strftime('%H:%M:%S')})\n")
                        f.write(f"{msg.content}\n")
                        if msg.voice_gender or msg.emotion:
                            f.write(f"    Voice: {msg.voice_gender}, Emotion: {msg.emotion}\n")
                        f.write("\n")
                
                # Add timing statistics
                f.write("\n" + "=" * 60 + "\n")
                f.write("CLAUDE OPUS 4 TIMING PERFORMANCE STATISTICS\n")
                f.write("=" * 60 + "\n")
                
                stats = self.get_timing_statistics()
                if stats:
                    f.write(f"Total Conversations: {stats['total_conversations']}\n")
                    f.write(f"Average Total Latency: {stats['avg_total_latency']:.2f}s\n")
                    f.write(f"Best Response Time: {stats['min_total_latency']:.2f}s\n")
                    f.write(f"Worst Response Time: {stats['max_total_latency']:.2f}s\n")
                    f.write(f"Average STT Duration: {stats['avg_stt_duration']:.2f}s\n")
                    f.write(f"Average Claude Opus 4 Duration: {stats['avg_claude_duration']:.2f}s\n")
                    f.write(f"Average TTS Duration: {stats['avg_tts_duration']:.2f}s\n")
                else:
                    f.write("No timing data available\n")
            
            logger.info(f"Claude session transcript saved to: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to save transcript: {e}")
            return ""
    
    def reset_session(self):
        """Reset conversation session"""
        self.session_memory.clear()
        self.timing_history.clear()
        # Re-add system message
        self.session_memory.append(ConversationMessage(
            role="system",
            content=self.system_prompt,
            timestamp=datetime.now()
        ))
        logger.info("Claude session reset")
    
    def run_conversation_loop(self):
        """
        Main conversation loop with timing measurements (Claude Opus 4 only)
        """
        print("🇴🇲 Omani Therapist AI - Claude Opus 4 Edition")
        print("=" * 60)
        print("🤖 Powered by Claude Opus 4 (claude-opus-4-20250514)")
        print("🎤 Speak in Arabic to begin conversation")
        print("🔊 The AI will respond in Omani Arabic")
        print("💬 Say 'انتهى' or 'exit' to end the session")
        print("🔄 Say 'بداية جديدة' to reset the conversation")
        print("⏱️  Performance timing will be measured and reported")
        print("=" * 60)
        
        # Welcome message
        welcome_msg = "أهلاً وسهلاً بك في جلسة العلاج النفسي مع كلود أوبوس 4. أنا هنا لمساعدتك والاستماع إليك بأحدث التقنيات. كيف حالك اليوم؟"
        self.speak_text(welcome_msg, self.default_voice_gender, "encouraging")
        
        conversation_count = 0
        
        try:
            while True:
                print("\n" + "-" * 40)
                
                # Get user speech with timing
                user_input, timing_metrics = self.get_user_speech(timeout_seconds=15)
                
                if not user_input or not timing_metrics:
                    print("⏰ No speech detected. Trying again...")
                    continue
                
                # Check for exit commands
                if any(word in user_input.lower() for word in ['انتهى', 'exit', 'bye', 'وداعا']):
                    print("👋 Ending Claude session...")
                    
                    # Print final timing statistics
                    self.print_timing_statistics()
                    
                    # Farewell message
                    farewell_msg = "شكراً لك على الجلسة مع كلود أوبوس 4. أتمنى أن تكون مفيدة. إلى اللقاء، وأتمنى لك كل الخير."
                    self.speak_text(farewell_msg, self.default_voice_gender, "calm")
                    
                    # Save transcript
                    transcript_file = self.save_session_transcript()
                    if transcript_file:
                        print(f"📄 Claude session transcript saved: {transcript_file}")
                    
                    break
                
                # Check for reset command
                if any(word in user_input.lower() for word in ['بداية جديدة', 'reset', 'start over']):
                    print("🔄 Resetting Claude conversation...")
                    self.reset_session()
                    
                    reset_msg = "حسناً، لنبدأ من جديد مع كلود أوبوس 4. كيف يمكنني مساعدتك اليوم؟"
                    self.speak_text(reset_msg, self.default_voice_gender, "encouraging")
                    conversation_count = 0
                    continue
                
                # Get AI response with timing
                ai_response = self.get_ai_response(user_input, timing_metrics)
                
                if ai_response:
                    # Speak the response with timing
                    success = self.speak_text(ai_response, self.default_voice_gender, self.default_emotion, timing_metrics)
                    
                    if success:
                        conversation_count += 1
                        
                        # Add completed timing metrics to history
                        self.timing_history.append(timing_metrics)
                        
                        # Print timing report for this turn
                        timing_metrics.print_timing_report()
                        
                        print(f"✅ Claude conversation turn {conversation_count} completed")
                    else:
                        print("❌ Failed to speak response")
                        # Still continue the conversation
                        
                else:
                    print("🚨 Claude Opus 4 failed to generate response")
                    # Fallback response
                    fallback_msg = "أعتذر، واجهت مشكلة تقنية. هل يمكنك إعادة السؤال؟"
                    self.speak_text(fallback_msg, self.default_voice_gender, "neutral")
                
                # Brief pause between turns
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n🛑 Claude conversation interrupted by user")
            
            # Print final timing statistics
            self.print_timing_statistics()
            
            # Save transcript
            transcript_file = self.save_session_transcript()
            if transcript_file:
                print(f"📄 Claude session transcript saved: {transcript_file}")
                
        except Exception as e:
            logger.error(f"Claude conversation loop error: {e}")
            print(f"🚨 Claude conversation error: {e}")
            
        finally:
            print("🏁 Claude Opus 4 conversation ended")


def main():
    """Main function to run the Omani Therapist AI with Claude Opus 4 only"""
    print("Omani Therapist AI - Claude Opus 4 Edition")
    print("=" * 60)
    
    # Check environment variables
    required_vars = ['AZURE_SPEECH_KEY', 'ANTHROPIC_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set up your .env file with:")
        print("   AZURE_SPEECH_KEY=your_azure_key")
        print("   AZURE_SPEECH_REGION=uaenorth")
        print("   ANTHROPIC_API_KEY=your_anthropic_key")
        return
    
    try:
        # Initialize the Claude-only AI system
        therapist_ai = OmaniTherapistAI_OnlyClaude()
        
        # Run the conversation loop
        therapist_ai.run_conversation_loop()
        
    except Exception as e:
        logger.error(f"System initialization error: {e}")
        print(f"🚨 Failed to initialize Claude system: {e}")
        print("\nTroubleshooting:")
        print("1. Verify your Azure Speech Services credentials")
        print("2. Verify your Anthropic API key")
        print("3. Check your internet connection")
        print("4. Ensure microphone permissions are enabled")
        print("5. Install required dependencies: pip install anthropic azure-cognitiveservices-speech pygame python-dotenv")


if __name__ == "__main__":
    main() 