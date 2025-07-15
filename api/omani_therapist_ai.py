#!/usr/bin/env python3
"""
Omani Therapist AI Conversation System
=====================================

This system integrates:
- Speech-to-Text (STT) for Arabic speech recognition
- OpenAI GPT-4o with Claude fallback for therapeutic conversations
- Text-to-Speech (TTS) for natural Omani Arabic responses
- Session memory management
- Culturally-sensitive therapeutic conversations
- Performance timing measurements

Author: AI Assistant
Created: 2025
"""

import os
import json
import time
import logging
import re
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple, cast
from dataclasses import dataclass, asdict
import io
import tempfile
import wave
import struct
from pydub import AudioSegment

# Azure Speech Services
import azure.cognitiveservices.speech as speechsdk

# AI Services
try:
    import openai
    from openai.types.chat import ChatCompletionMessageParam
except ImportError:
    openai = None
    ChatCompletionMessageParam = None

try:
    import anthropic
except ImportError:
    anthropic = None

# Audio playback
import pygame

# Advanced Emotion Refinement
try:
    from emotion_refiner import EmotionRefiner, EmotionContext, RefinedResponse
except ImportError:
    EmotionRefiner = None
    EmotionContext = None
    RefinedResponse = None

# Environment variables
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv(dotenv_path='../../.env')  # Look for .env in project root
load_dotenv()  # Also check current directory as fallback

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
        print("⏱️  TIMING PERFORMANCE REPORT")
        print("=" * 50)
        print(f"🎤 Speech Recognition: {self.stt_duration:.2f}s")
        print(f"🤖 AI Processing:     {self.ai_processing_duration:.2f}s")
        print(f"🔊 TTS Synthesis:     {self.tts_duration:.2f}s")
        print(f"📊 TOTAL LATENCY:     {self.total_latency:.2f}s")
        print("=" * 50)


class OmaniTherapistAI:
    """
    Main conversation agent that integrates STT, AI, and TTS
    for therapeutic conversations in Omani Arabic with performance timing
    """
    
    def __init__(self):
        """Initialize the Omani Therapist AI system"""
        # Load API keys from environment ##############################################################################################################################
        self.azure_speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.azure_region = os.getenv('AZURE_SPEECH_REGION', 'uaenorth')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Try backup Azure key if primary not found
        if not self.azure_speech_key:
            self.azure_speech_key = os.getenv('AZURE_SPEECH_KEY_BACKUP')
        
        # Validate required credentials
        if not self.azure_speech_key:
            raise ValueError("Azure Speech Key not found. Please set AZURE_SPEECH_KEY in environment variables.")
        
        if not self.openai_api_key:
            logger.warning("OpenAI API key not found. Only Claude fallback will be available.")
        
        if not self.anthropic_api_key:
            logger.warning("Anthropic API key not found. No fallback available if OpenAI fails.")
        
        # Initialize AI clients
        if self.openai_api_key and openai:
            openai.api_key = self.openai_api_key
            self.openai_client = openai
        
        if self.anthropic_api_key and anthropic:
            try:
                # Initialize Anthropic client according to official documentation
                self.claude_client = anthropic.Anthropic(
                    api_key=self.anthropic_api_key
                )
                logger.info("Anthropic client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic client: {e}")
                self.claude_client = None
        else:
            self.claude_client = None
        
        # Initialize Azure Speech services
        self._setup_azure_speech()
        
        # Initialize pygame for audio playback
        pygame.mixer.init(frequency=48000, size=-16, channels=1, buffer=1024)
        
        # Session memory (list of ConversationMessage objects)
        self.session_memory: List[ConversationMessage] = []
        self.max_memory_turns = 10  # Keep last 10 exchanges
        
        # Timing metrics storage
        self.timing_history: List[TimingMetrics] = []
        
        # Enhanced therapeutic system prompts with detailed cultural guidelines ###############################################################
        self.system_prompt_arabic = """أنت دكتور نفسي عماني متخصص ومتفهم، تعمل كمساعد للعلاج النفسي مع الحفاظ على الثقافة العمانية والإسلامية. تجيب دائماً باللغة العربية العمانية الأصيلة، وتستخدم لغة حساسة ثقافياً ومراعية للأسرة والإيمان والتقاليد العمانية.

## المبادئ الأساسية: 

### 1. الهوية الثقافية والدينية:
- استخدم اللهجة العمانية الأصيلة والتعابير المحلية
- احترم القيم الإسلامية والتقاليد العمانية
- اعتبر أهمية الأسرة والمجتمع في الشفاء النفسي
- استخدم المفاهيم الإسلامية مثل الصبر، التوكل، والرضا بالقضاء والقدر
- تذكر أن طلب المساعدة النفسية قوة وليس ضعف في الإسلام

### 2. النهج العلاجي المتكامل:
- **العلاج المعرفي السلوكي (CBT)**: مكيف مع الثقافة العمانية
- **العلاج الإسلامي**: استخدم الآيات والأحاديث المناسبة للراحة النفسية
- **العلاج الأسري**: اعتبر دور الأسرة في الدعم والشفاء
- **التأمل والذكر**: شجع على الصلاة والذكر كوسائل للهدوء النفسي

### 3. الحساسية الثقافية:
- **شرف العائلة**: تعامل بحذر مع القضايا التي قد تؤثر على سمعة الأسرة
- **الأدوار الاجتماعية**: احترم الأدوار التقليدية للرجل والمرأة
- **الخصوصية**: احترم الحاجة للكتمان في بعض المواضيع الحساسة
- **التواصل غير المباشر**: استخدم الأسلوب المهذب والغير مباشر عند الحاجة

### 4. التعامل مع القضايا الشائعة:
- **القلق والتوتر**: ربطها بالتوكل على الله والصبر
- **الاكتئاب**: استخدم مفهوم الابتلاء والأجر من الله
- **المشاكل الأسرية**: شجع على الحوار والتفاهم والاحترام المتبادل
- **ضغوط العمل**: وازن بين الطموح والرضا بالرزق
- **مشاكل الشباب**: فهم تحديات الجيل الجديد مع احترام التقاليد

### 5. العبارات والتعابير العمانية:
- "إن شاء الله بيكون خير" للتشجيع
- "الصبر مفتاح الفرج" للتهدئة
- "الله يعطيك القوة" للدعم
- "هذا امتحان من الله" للابتلاءات
- "اطلب المساعدة عادي، مافي عيب" لتشجيع طلب المساعدة

### 6. بروتوكول الأزمات:
إذا ذكر المستخدم أفكار إيذاء النفس أو الانتحار:
- تعامل بجدية تامة وتعاطف
- ذكره بحرمة إيذاء النفس في الإسلام
- شجعه على طلب المساعدة الفورية
- اعطه أرقام الطوارئ العمانية
- ذكره بأن الله يحبه وأن حياته لها معنى وقيمة

### 7. حدود المساعدة:
- أنت مساعد ذكي وليس بديل عن الطبيب النفسي المتخصص
- شجع على زيارة المختصين عند الحاجة
- لا تعطي تشخيصات طبية أو وصفات دوائية
- احترم خصوصية المستخدم ولا تحفظ معلومات شخصية

كن دائماً متعاطف، مهني، ومحترم للثقافة العمانية والإسلامية."""

###############################################################

        self.system_prompt_english = """You are a specialized and understanding Omani therapist, working as a mental health assistant while preserving Omani and Islamic culture. You always respond in English, using culturally sensitive language that respects family, faith, and Omani traditions.

## Core Principles:

### 1. Cultural and Religious Identity:
- Respect Islamic values and Omani traditions
- Consider the importance of family and community in mental healing
- Use Islamic concepts like patience (sabr), trust in God (tawakkul), and acceptance of fate (ridha bil qada wal qadar)
- Remember that seeking mental help is a strength, not weakness in Islam

### 2. Integrated Therapeutic Approach:
- **Cognitive Behavioral Therapy (CBT)**: Adapted for Omani culture
- **Islamic Therapy**: Use appropriate verses and hadiths for psychological comfort
- **Family Therapy**: Consider the family's role in support and healing
- **Meditation and Dhikr**: Encourage prayer and remembrance as means of mental peace

### 3. Cultural Sensitivity:
- **Family Honor**: Handle issues that may affect family reputation with care
- **Social Roles**: Respect traditional roles of men and women
- **Privacy**: Respect the need for confidentiality in sensitive topics
- **Indirect Communication**: Use polite and indirect approach when needed

### 4. Dealing with Common Issues:
- **Anxiety and Stress**: Connect them to trust in God and patience
- **Depression**: Use the concept of trials (ibtila) and reward from God
- **Family Problems**: Encourage dialogue, understanding, and mutual respect
- **Work Pressure**: Balance between ambition and contentment with provisions
- **Youth Issues**: Understand new generation challenges while respecting traditions

### 5. Supportive Phrases:
- "God willing, it will be good" for encouragement
- "Patience is the key to relief" for calming
- "May God give you strength" for support
- "This is a test from God" for trials
- "Seeking help is normal, there's no shame" to encourage seeking help

### 6. Crisis Protocol:
If the user mentions self-harm or suicidal thoughts:
- Deal with complete seriousness and empathy
- Remind them that harming oneself is forbidden in Islam
- Encourage seeking immediate help
- Provide Omani emergency numbers
- Remind them that God loves them and their life has meaning and value

### 7. Limits of Assistance:
- You are an AI assistant, not a replacement for a specialized therapist
- Encourage visiting specialists when needed
- Don't provide medical diagnoses or prescriptions
- Respect user privacy and don't store personal information

Always be empathetic, professional, and respectful of Omani and Islamic culture."""

        # Default system prompt (Arabic)
        self.system_prompt = self.system_prompt_arabic
        
        # Add system message to memory
        self.session_memory.append(ConversationMessage(
            role="system",
            content=self.system_prompt,
            timestamp=datetime.now()
        ))
        
        # Available voices for both languages
        self.voices = {
            'ar': {
            'male': 'ar-OM-AbdullahNeural',  ###############################################################
            'female': 'ar-OM-AyshaNeural' ###############################################################
            },
            'en': {
                'male': 'en-US-BrianNeural', ###############################################################
                'female': 'en-US-JennyNeural' ###############################################################
            }
        }
        
        # Default settings
        self.default_voice_gender = "male"
        self.default_emotion = "neutral"
        
        # Initialize Advanced Emotion Refinement (GPT-4.1-nano)
        self.emotion_refiner = None
        self.use_emotion_refinement = False
        if EmotionRefiner and self.openai_api_key:
            try:
                self.emotion_refiner = EmotionRefiner(self.openai_api_key)
                self.use_emotion_refinement = True
                logger.info("✨ Advanced Emotion Refinement enabled (GPT-4.1-nano)")
            except Exception as e:
                logger.warning(f"Failed to initialize EmotionRefiner: {e}")
        else:
            logger.info("Advanced Emotion Refinement disabled (missing dependencies)")
        
        logger.info("Omani Therapist AI initialized successfully")
    
    def detect_language(self, text: str) -> str:
        """
        Detect if the input text is primarily in English or Arabic
        
        Args:
            text: Input text to analyze
            
        Returns:
            'en' for English, 'ar' for Arabic (default)
        """
        if not text or not text.strip():
            return 'ar'  # Default to Arabic
        
        # Clean text for analysis
        text = text.strip().lower()
        
        # Count Arabic characters (including Arabic numerals)
        arabic_chars = len(re.findall(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text))
        
        # Count English characters (Latin alphabet)
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        # Count total meaningful characters (excluding spaces and punctuation)
        total_chars = arabic_chars + english_chars
        
        # If no meaningful characters, default to Arabic
        if total_chars == 0:
            return 'ar'
        
        # Calculate English ratio
        english_ratio = english_chars / total_chars
        
        # Debug logging
        logger.info(f"Language detection - Arabic chars: {arabic_chars}, English chars: {english_chars}, English ratio: {english_ratio:.2f}")
        
        # If more than 50% English characters AND has some English content, consider it English
        if english_ratio > 0.5 and english_chars > 3:
            logger.info("Detected English input")
            return 'en'
        
        # Check for common English words/phrases
        english_indicators = ['hello', 'hi', 'hey', 'how are you', 'thank you', 'yes', 'no', 'can you', 'i am', 'help me']
        text_lower = text.lower()
        english_word_count = sum(1 for indicator in english_indicators if indicator in text_lower)
        
        if english_word_count >= 1 and english_ratio > 0.3:
            logger.info("Detected English based on common words")
            return 'en'
        
        # Otherwise, default to Arabic
        logger.info("Detected Arabic input")
        return 'ar'
    
    def detect_emotion_from_text(self, text: str) -> str:
        """
        Detect appropriate emotion for TTS based on the content of AI response
        
        Args:
            text: AI response text to analyze
            
        Returns:
            Detected emotion: 'calm', 'encouraging', 'excited', 'sad', 'neutral'
        """
        if not text or not text.strip():
            return 'neutral'
        
        text_lower = text.lower()
        
        # Arabic and English patterns for different emotions
        emotion_patterns = {
            'encouraging': [
                # Arabic encouraging patterns
                r'\b(تستطيع|قادر|قوي|ممتاز|رائع|أحسنت|موفق|إن شاء الله بيكون خير|تقدر)\b',
                r'\b(لا تخاف|لا تقلق|أنت بخير|راح يكون أحسن|استمر|امشي قدام)\b',
                r'\b(أنت قوي|عندك قوة|فيك أمل|الله معاك|ثق بنفسك)\b',
                # English encouraging patterns  
                r'\b(you can|you\'re capable|strong|excellent|great|keep going|trust yourself)\b',
                r'\b(don\'t worry|don\'t fear|you\'re doing well|it will get better|believe in yourself)\b',
                r'\b(proud of you|you\'ve got this|stay positive|you\'re on the right track)\b'
            ],
            'excited': [
                # Arabic excited patterns
                r'\b(مبروك|تهانينا|ممتاز جداً|رائع جداً|أحسنت|هذا رائع|عظيم|فرحان لك)\b',
                r'\b(ما شاء الله|الله يبارك فيك|هذا إنجاز عظيم|تطور رائع)\b',
                # English excited patterns
                r'\b(congratulations|amazing|fantastic|wonderful|excellent|great job|awesome)\b',
                r'\b(so proud|incredible progress|breakthrough|outstanding|brilliant)\b',
                r'[!]{2,}|[؟]{2,}'  # Multiple exclamation marks
            ],
            'sad': [
                # Arabic sad/empathetic patterns  
                r'\b(أتفهم ألمك|أعرف أنه صعب|هذا مؤلم|أحس بيك|أحزن لك)\b',
                r'\b(صعب عليك|تعبان|حزين|ألم|معاناة|صبر|ابتلاء)\b',
                r'\b(أسف لما تمر به|الله يصبرك|الله يعينك|أدعو لك)\b',
                # English sad/empathetic patterns
                r'\b(I understand your pain|I know it\'s hard|I\'m sorry you\'re going through|I feel for you)\b',
                r'\b(difficult|painful|struggling|heartbroken|grieving|loss|suffering)\b',
                r'\b(my heart goes out|sending you strength|you\'re not alone in this)\b'
            ],
            'calm': [
                # Arabic calm patterns
                r'\b(هدوء|استرخي|تنفس|سكينة|طمأنينة|اهدأ|خذ وقتك)\b',
                r'\b(بالهدوء|بروية|ببطء|خطوة بخطوة|واحدة واحدة)\b',
                r'\b(التأمل|الصلاة|الذكر|الاستغفار|السكينة|الطمأنينة)\b',
                # English calm patterns  
                r'\b(calm|relax|breathe|peaceful|serenity|take your time|slowly)\b',
                r'\b(meditation|mindfulness|deep breath|settle|center yourself)\b',
                r'\b(step by step|one moment at a time|gently|softly)\b'
            ]
        }
        
        # Check each emotion pattern
        for emotion, patterns in emotion_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return emotion
        
        # Default emotion based on punctuation and context
        if '!' in text or '؟' in text:
            return 'encouraging'
        elif '...' in text or 'سكت' in text_lower:
            return 'calm'
        else:
            return 'neutral'
    
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

    def get_user_speech_from_file(self, file_path: str) -> Tuple[Optional[str], Optional[TimingMetrics]]:
        """
        Process user speech from an audio file and convert to text.
        This method relies on the Speech SDK's ability to handle various formats.

        Args:
            file_path: Path to the audio file.

        Returns:
            Tuple of (recognized text or None, timing metrics or None)
        """
        try:
            speech_start_time = time.time()
            
            # Configure audio input from file
            audio_config = speechsdk.AudioConfig(filename=file_path)

            # Create speech recognizer
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.stt_config,
                audio_config=audio_config
            )

            # Start recognition. The .get() method waits for the async operation to complete.
            future = recognizer.recognize_once_async()
            result = future.get()
            
            speech_end_time = time.time()
            
            timing = TimingMetrics(
                speech_start_time=speech_start_time,
                speech_end_time=speech_end_time,
                ai_processing_start_time=0,
                ai_processing_end_time=0,
                tts_start_time=0,
                tts_end_time=0,
                voice_playback_start_time=0
            )

            if result is None:
                logger.error("Speech recognition result is None.")
                return None, timing

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                logger.info(f"✅ STT recognized from file: '{result.text}'")
                return result.text, timing
            elif result.reason == speechsdk.ResultReason.NoMatch:
                logger.warning(f"No speech could be recognized from file: {file_path}")
                return None, timing
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logger.error(f"Speech recognition canceled for file {file_path}: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"Error details: {cancellation.error_details}")
                return None, timing
            
            return None, timing # Default return

        except Exception as e:
            logger.error(f"Error recognizing speech from file {file_path}: {e}", exc_info=True)
            return None, None
    
    def _prepare_messages_for_ai(self) -> List[Dict[str, str]]:
        """
        Prepare recent conversation history for AI API call
        
        Returns:
            List of message dictionaries for API
        """
        # Get recent messages (last N turns)
        recent_messages = self.session_memory[-self.max_memory_turns:]
        
        # Convert to API format
        api_messages = []
        for msg in recent_messages:
            api_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        return api_messages
    
    def _call_openai_gpt4(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Call OpenAI GPT-4o API for response"""
        if not self.openai_client:
            logger.warning("OpenAI client not initialized, cannot make call.")
            return None
        
        try:
            logger.info("🤖 Calling OpenAI GPT-4o...") ###############################################################
            
            typed_messages = cast(List[ChatCompletionMessageParam], messages)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4.1-mini", ############################################################### gpt-4.1/ gpt-4.1-mini /gpt-4o
                messages=typed_messages,
                temperature=0.7,
                max_tokens=500
            )
            
            if response.choices and response.choices[0].message:
                ai_response = response.choices[0].message.content or ""
                logger.info("✅ OpenAI response received")
                return ai_response.strip()
                
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
        
        return None

    def _call_claude_fallback(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Fallback to Anthropic Claude 3 Sonnet if OpenAI fails"""
        if not self.claude_client or not anthropic:
            logger.warning("Anthropic client not available for fallback.")
            return None
            
        try:
            logger.info("🤖 Calling Anthropic Claude 3 Sonnet (fallback)...")
            
            # Filter out the system message for Claude if it's the first message
            if messages and messages[0]['role'] == 'system':
                system_prompt = messages[0]['content']
                user_messages = messages[1:]
            else:
                system_prompt = self.system_prompt # Default system prompt
                user_messages = messages

            typed_user_messages = cast(List[Any], user_messages)

            response = self.claude_client.messages.create(
                model="claude-4-opus-20250520",  # Updated to Claude Opus 4  ###############################################################
                system=system_prompt,
                messages=typed_user_messages,
                max_tokens=500,  # Increased for better responses
                temperature=0.7
            )
            
            if response.content and isinstance(response.content, list):
                content_block = response.content[0]
                if isinstance(content_block, anthropic.types.TextBlock):
                    ai_response = content_block.text
                    logger.info("✅ Anthropic fallback response received")
                    return ai_response.strip()

        except Exception as e:
            logger.error(f"Anthropic API call failed: {e}")
            
        return None

    def get_ai_response(self, user_input: str, timing_metrics: TimingMetrics) -> Tuple[Optional[str], str]:
        """
        Get AI response with OpenAI primary and Claude fallback
        
        Args:
            user_input: User's input text
            timing_metrics: Timing metrics object to update
            
        Returns:
            Tuple of (AI response or None if all services failed, detected language)
.        """
        # Record AI processing start time
        timing_metrics.ai_processing_start_time = time.time()
        
        # Detect language of user input
        detected_language = self.detect_language(user_input)
        logger.info(f"Detected language: {detected_language} for input: {user_input[:50]}...")
        
        # Set appropriate system prompt based on detected language
        if detected_language == 'en':  ###############################################################  english
            self.system_prompt = self.system_prompt_english
            logger.info("Using English system prompt")
        else:   ###############################################################  arabic
            self.system_prompt = self.system_prompt_arabic
            logger.info("Using Arabic system prompt")
        
        # Update system message in session memory if language changed
        if self.session_memory and self.session_memory[0].role == "system":
            self.session_memory[0].content = self.system_prompt
        
        # Add user message to session memory
        self.session_memory.append(ConversationMessage(
            role="user",
            content=user_input,
            timestamp=datetime.now()
        ))
        
        # Prepare messages for AI
        messages = self._prepare_messages_for_ai()
        
        # Try OpenAI first
        ai_response = self._call_openai_gpt4(messages)
        
        # Fallback to Claude if OpenAI fails
        if not ai_response:
            logger.info("🔄 Falling back to Claude...")
            ai_response = self._call_claude_fallback(messages)
        
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
        
        return ai_response, detected_language
    
    def refine_ai_response_with_emotion(self, ai_response: str, user_input: str, detected_language: str) -> Tuple[str, str]:
        """
        Stage 2: Advanced emotion refinement using GPT-4.1-nano
        Transforms raw AI response into naturally expressive, therapeutically appropriate speech
        
        Args:
            ai_response: Raw AI response from Stage 1
            user_input: Original user input for context
            detected_language: Detected language (ar/en)
            
        Returns:
            Tuple of (refined_response_text, enhanced_ssml)
        """
        if not self.use_emotion_refinement or not self.emotion_refiner:
            # Fallback to basic emotion detection
            basic_emotion = self.detect_emotion_from_text(ai_response)
            return ai_response, self._create_ssml_text(ai_response, basic_emotion, language=detected_language)
        
        try:
            # Detect user emotional state for context
            user_emotion = self.detect_emotion_from_text(user_input)
            
            # Determine crisis level from conversation history
            crisis_level = self._assess_crisis_level()
            
            # Determine therapeutic stage
            therapeutic_stage = self._assess_therapeutic_stage()
            
            # Create emotion context for GPT-4.1-nano
            if EmotionContext is None:
                raise ImportError("EmotionContext not available")
            
            emotion_context = EmotionContext(
                user_emotional_state=user_emotion,
                conversation_history=self._get_recent_conversation_for_context(),
                crisis_level=crisis_level,
                cultural_context='omani' if detected_language == 'ar' else 'english',
                therapeutic_stage=therapeutic_stage
            )
            
            # Call GPT-4.1-nano for advanced emotion refinement
            logger.info(f"🎨 Refining response with GPT-4.1-nano (user emotion: {user_emotion}, crisis: {crisis_level})")
            refined_result = self.emotion_refiner.refine_emotional_response(ai_response, emotion_context)
            
            if refined_result.confidence_score > 0.5:
                logger.info(f"✨ Emotion refinement successful: {len(refined_result.emotion_enhancements)} enhancements")
                logger.info(f"🎭 Enhancements: {', '.join(refined_result.emotion_enhancements)}")
                
                # Always create our own SSML structure - don't use the emotion refiner's SSML directly
                # The emotion refiner's SSML might be a complete document which would conflict with our structure
                enhanced_ssml = self._create_ssml_text(
                    refined_result.refined_response, user_emotion, language=detected_language
                )
                
                return refined_result.refined_response, enhanced_ssml
            else:
                logger.warning(f"Low confidence refinement ({refined_result.confidence_score:.2f}), using original response")
                
        except Exception as e:
            logger.error(f"Emotion refinement failed: {e}")
        
        # Fallback to basic emotion detection and SSML
        basic_emotion = self.detect_emotion_from_text(ai_response)
        return ai_response, self._create_ssml_text(ai_response, basic_emotion, language=detected_language)
    
    def _assess_crisis_level(self) -> str:
        """Assess crisis level from recent conversation"""
        if not self.session_memory:
            return 'none'
        
        # Check last few user messages for crisis indicators
        recent_user_messages = [msg.content for msg in self.session_memory[-6:] if msg.role == 'user']
        crisis_keywords = {
            'severe': ['أريد أن أموت', 'أقتل نفسي', 'suicide', 'kill myself', 'end it all'],
            'moderate': ['لا أستطيع', 'يائس', 'مكتئب جداً', 'can\'t take it', 'hopeless', 'severely depressed'],
            'mild': ['حزين', 'قلق', 'صعب', 'sad', 'anxious', 'difficult', 'struggling']
        }
        
        text = ' '.join(recent_user_messages).lower()
        
        for level, keywords in crisis_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return level
        
        return 'none'
    
    def _assess_therapeutic_stage(self) -> str:
        """Assess current therapeutic stage from conversation length and content"""
        if len(self.session_memory) <= 4:
            return 'rapport_building'
        elif len(self.session_memory) <= 12:
            return 'exploration'
        elif len(self.session_memory) <= 20:
            return 'intervention'
        else:
            return 'closure'
    
    def _get_recent_conversation_for_context(self) -> List[Dict[str, str]]:
        """Get recent conversation history for emotion context"""
        recent = []
        for msg in self.session_memory[-8:]:  # Last 8 messages for context
            recent.append({
                'role': msg.role,
                'content': msg.content[:200] + '...' if len(msg.content) > 200 else msg.content,  # Truncate long messages
                'timestamp': msg.timestamp.isoformat()
            })
        return recent
    
    def _adjust_settings_for_crisis(self, settings: Dict[str, str], crisis_level: str) -> Dict[str, str]:
        """Adjust TTS settings based on crisis level for more appropriate therapeutic tone"""
        # Create a copy to avoid modifying the original
        adjusted_settings = settings.copy()
        
        if crisis_level == 'severe':
            # For severe crisis: slower, lower pitch, softer volume for calm, reassuring tone
            adjusted_settings['rate'] = '-15%'
            adjusted_settings['pitch'] = '-10%'
            adjusted_settings['volume'] = 'soft'
        elif crisis_level == 'moderate':
            # For moderate crisis: slightly slower, slightly lower pitch
            adjusted_settings['rate'] = '-8%'
            adjusted_settings['pitch'] = '-6%'
            adjusted_settings['volume'] = 'soft'
        elif crisis_level == 'mild':
            # For mild crisis: slightly slower for reassurance
            adjusted_settings['rate'] = '-3%'
            adjusted_settings['pitch'] = '-2%'
            
        return adjusted_settings
    
    def _create_ssml_text(self, text: str, emotion: str = "neutral", 
                         voice_name: Optional[str] = None, language: str = "ar") -> str:
        """Create SSML formatted text with emotional control and crisis-based adjustments"""
        if not voice_name:
            voice_name = self.voices[language][self.default_voice_gender]
        
        # Emotion-specific prosody settings - optimized for natural human-like speech
        # Based on Azure TTS best practices to avoid chipmunk/robotic effects
        emotion_settings = {
            'calm': {'rate': '-5%', 'pitch': '-5%', 'volume': 'soft'},
            'encouraging': {'rate': '+10%', 'pitch': '+8%', 'volume': 'medium'},
            'excited': {'rate': '+15%', 'pitch': '+12%', 'volume': 'medium'},  # Reduced from +35%/+25% to avoid chipmunk effect
            'sad': {'rate': '-10%', 'pitch': '-8%', 'volume': 'soft'},  # Reduced from -20%/-15% to be less robotic
            'neutral': {'rate': 'medium', 'pitch': 'medium', 'volume': 'medium'}
        }
        
        settings = emotion_settings.get(emotion, emotion_settings['neutral'])
        
        # Crisis-based pitch and tone adjustments
        crisis_level = self._assess_crisis_level()
        if crisis_level != 'none':
            settings = self._adjust_settings_for_crisis(settings, crisis_level)
        
        # Set appropriate xml:lang based on language parameter
        xml_lang = "ar-OM" if language == "ar" else "en-US"
        
        # Add natural pauses for better human-like speech
        enhanced_text = self._add_natural_pauses(text, emotion)
        
        # Clean the enhanced text to ensure no malformed SSML tags
        enhanced_text = self._clean_ssml_content(enhanced_text)
        
        ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{xml_lang}">
            <voice name="{voice_name}">
                <prosody rate="{settings['rate']}" pitch="{settings['pitch']}" volume="{settings['volume']}">
                    {enhanced_text}
                </prosody>
            </voice>
        </speak>"""
        
        return ssml.strip()
    
    def _clean_ssml_content(self, text: str) -> str:
        """Clean text content to ensure valid SSML structure"""
        import re
        
        # Remove any complete SSML documents that might be embedded
        text = re.sub(r'<\?xml[^>]*\?>', '', text)  # Remove XML declarations
        
        # Remove any stray SSML tags that might cause conflicts
        text = re.sub(r'</?speak[^>]*>', '', text)  # Remove any speak tags
        text = re.sub(r'</?voice[^>]*>', '', text)  # Remove any voice tags
        text = re.sub(r'</?prosody[^>]*>', '', text)  # Remove any prosody tags
        
        # Fix malformed break tags (like bbreak)
        text = re.sub(r'<bbreak\s+time="([^"]+)"\s*/?>', r'<break time="\1"/>', text)
        text = re.sub(r'<break\s+time=\'([^\']+)\'\s*/?>', r'<break time="\1"/>', text)  # Fix single quotes
        
        # Ensure break tags are properly formatted
        text = re.sub(r'<break\s+time="([^"]+)"\s*/?>', r'<break time="\1"/>', text)
        
        # Remove any malformed emphasis tags and replace with proper ones if needed
        text = re.sub(r'</?emphasis[^>]*>', '', text)
        
        # Remove any other potentially problematic SSML tags
        text = re.sub(r'</?phoneme[^>]*>', '', text)
        text = re.sub(r'</?say-as[^>]*>', '', text)
        text = re.sub(r'</?sub[^>]*>', '', text)
        
        # Clean up any double spaces or line breaks
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _add_natural_pauses(self, text: str, emotion: str) -> str:
        """Add natural pauses and breaks to text based on emotion for more human-like speech
        
        Enhanced to handle complex emotion markers from GPT-4.1-nano refinement:
        - Converts emotion markers like '*soft sigh*' to proper SSML breaks
        - Handles both English and Arabic emotional expressions
        - Removes unwanted text markers that would be spoken aloud
        """
        import re
        
        # STAGE 1: Handle complex emotion markers from GPT-4.1-nano refinement
        # These need to be converted to SSML breaks instead of being spoken
        
        # English emotion markers
        emotion_patterns = {
            # Sigh variations
            r'\*soft sigh\*': '<break time="500ms"/>',
            r'\*gentle sigh\*': '<break time="450ms"/>',
            r'\*deep sigh\*': '<break time="600ms"/>',
            r'\*relieved sigh\*': '<break time="400ms"/>',
            r'\*tired sigh\*/': '<break time="550ms"/>',
            r'\*sad sigh\*': '<break time="650ms"/>',
            r'\*thoughtful sigh\*': '<break time="500ms"/>',
            r'\*proud sigh\*': '<break time="400ms"/>',
            
            # Pause variations
            r'\*soft pause\*': '<break time="400ms"/>',
            r'\*gentle pause\*': '<break time="350ms"/>',
            r'\*thoughtful pause\*': '<break time="500ms"/>',
            r'\*encouraging pause\*': '<break time="300ms"/>',
            r'\*reassuring pause\*': '<break time="350ms"/>',
            r'\*contemplative pause\*': '<break time="550ms"/>',
            r'\*excited pause\*': '<break time="200ms"/>',
            r'\*calming pause\*': '<break time="450ms"/>',
            
            # Arabic emotion markers
            r'\*تنهد خفيف\*': '<break time="500ms"/>',  # soft sigh
            r'\*تنهد عميق\*': '<break time="600ms"/>',  # deep sigh
            r'\*تنهد حزين\*': '<break time="650ms"/>',  # sad sigh
            r'\*تنهد مطمئن\*': '<break time="400ms"/>',  # reassuring sigh
            r'\*وقفة خفيفة\*': '<break time="350ms"/>',  # soft pause
            r'\*وقفة مطمئنة\*': '<break time="350ms"/>',  # reassuring pause
            r'\*وقفة متأملة\*': '<break time="500ms"/>',  # contemplative pause
            r'\*وقفة مشجعة\*': '<break time="300ms"/>',  # encouraging pause
            r'\*وقفة فرحة\*': '<break time="250ms"/>',  # happy pause
            r'\*وقفة هادئة\*': '<break time="450ms"/>',  # calm pause
            
            # Breathing and grounding markers
            r'\*deep breath\*': '<break time="700ms"/>',
            r'\*breathe\*': '<break time="600ms"/>',
            r'\*inhale\*': '<break time="500ms"/>',
            r'\*exhale\*': '<break time="500ms"/>',
            r'\*تنفس عميق\*': '<break time="700ms"/>',  # deep breath
            r'\*شهيق\*': '<break time="500ms"/>',  # inhale
            r'\*زفير\*': '<break time="500ms"/>',  # exhale
            
            # Voice quality markers that should be removed
            r'\*whispered\*': '',
            r'\*softly\*': '',
            r'\*gently\*': '',
            r'\*warmly\*': '',
            r'\*quietly\*': '',
            r'\*بهمس\*': '',  # whispered
            r'\*بلطف\*': '',  # gently
            r'\*بحنان\*': '',  # warmly
        }
        
        # Apply emotion marker replacements
        for pattern, replacement in emotion_patterns.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # STAGE 2: Handle basic emotion expressions (existing functionality)
        # Replace ellipsis with natural pauses
        text = re.sub(r'\.{3,}', '<break time="800ms"/>', text)  # ...
        text = re.sub(r'_{3,}', '<break time="600ms"/>', text)   # ___
        
        # Add breathing/sigh effects for remaining simple emotional moments
        text = re.sub(r'<sigh>', '<break time="400ms"/>', text)
        text = re.sub(r'\*sigh\*', '<break time="400ms"/>', text)
        text = re.sub(r'\(sigh\)', '<break time="400ms"/>', text)
        
        # Handle hesitation markers
        text = re.sub(r'\buh+m+\b', '<break time="300ms"/>um<break time="200ms"/>', text, flags=re.IGNORECASE)
        text = re.sub(r'\bah+\b', '<break time="250ms"/>ah<break time="150ms"/>', text, flags=re.IGNORECASE)
        text = re.sub(r'\bwell\b', 'well<break time="200ms"/>', text, flags=re.IGNORECASE)
        text = re.sub(r'\byou know\b', 'you know<break time="150ms"/>', text, flags=re.IGNORECASE)
        
        # Arabic hesitation markers
        text = re.sub(r'\bيعني\b', 'يعني<break time="200ms"/>', text)  # "I mean"
        text = re.sub(r'\bأه\b', 'أه<break time="150ms"/>', text)     # "ah"
        text = re.sub(r'\bإم\b', 'إم<break time="200ms"/>', text)     # "um"
        
        # STAGE 3: Emotion-specific pause adjustments (existing functionality enhanced)
        if emotion == 'excited':
            # Quick, energetic pauses
            text = re.sub(r'([.!?])\s+', r'\1<break time="150ms"/> ', text)
            text = re.sub(r'(,)\s+', r'\1<break time="100ms"/> ', text)
        elif emotion in ['calm', 'sad']:
            # Longer, contemplative pauses
            text = re.sub(r'([.!?])\s+', r'\1<break time="400ms"/> ', text)
            text = re.sub(r'(,)\s+', r'\1<break time="250ms"/> ', text)
        else:
            # Default: moderate pauses
            text = re.sub(r'([.!?])\s+', r'\1<break time="300ms"/> ', text)
            text = re.sub(r'(,)\s+', r'\1<break time="150ms"/> ', text)
        
        # STAGE 4: Clean up any remaining unwanted markers
        # Remove any remaining asterisk markers that weren't caught above
        text = re.sub(r'\*[^*]*\*', '', text)  # Remove any remaining *text* patterns
        text = re.sub(r'\([^)]*pause[^)]*\)', '<break time="300ms"/>', text, flags=re.IGNORECASE)  # (pause variations)
        text = re.sub(r'\([^)]*sigh[^)]*\)', '<break time="400ms"/>', text, flags=re.IGNORECASE)  # (sigh variations)
        
        # Clean up multiple consecutive breaks
        text = re.sub(r'(<break time="[^"]*"/>\s*){2,}', r'<break time="600ms"/>', text)
        
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def speak_text(self, text: str, voice_gender: str = "female", 
                   emotion: str = "neutral", timing_metrics: Optional[TimingMetrics] = None, 
                   return_bytes: bool = False, language: str = "ar"):
        try:
            logger.info(f"🔊 TTS Request - Language: {language}, Voice: {voice_gender}, Emotion: {emotion}")
            logger.info(f"🔊 TTS Text: {text[:100]}...")
            
            if timing_metrics:
                timing_metrics.tts_start_time = time.time()
            
            # Get voice name
            voice_name = self.voices[language].get(voice_gender, self.voices[language]['female'])
            logger.info(f"🔊 Selected voice: {voice_name}")
            
            # Set voice in config
            self.tts_config.speech_synthesis_voice_name = voice_name
            
            # Create SSML
            ssml_text = self._create_ssml_text(text, emotion, voice_name, language)
            logger.info(f"🔊 Generated SSML: {ssml_text[:200]}...")
            
            # Create synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.tts_config,
                audio_config=None
            )
            
            # Perform synthesis
            logger.info("🔊 Starting TTS synthesis...")
            result = synthesizer.speak_ssml_async(ssml_text).get()
            
            if timing_metrics:
                timing_metrics.tts_end_time = time.time()
            
            if result is None:
                logger.error("❌ TTS synthesis result is None.")
                return None
                
            logger.info(f"🔊 TTS synthesis completed with reason: {result.reason}")
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info("✅ TTS synthesis successful")
                audio_size = len(result.audio_data) if result.audio_data else 0
                logger.info(f"🔊 Audio data size: {audio_size} bytes")
                
                if return_bytes:
                    logger.info("🔊 Returning audio bytes")
                    return result.audio_data
                else:
                    if result.audio_data:
                        logger.info("🔊 Playing audio via pygame")
                        if timing_metrics:
                            timing_metrics.voice_playback_start_time = time.time()
                        audio_stream = io.BytesIO(result.audio_data)
                        pygame.mixer.music.load(audio_stream)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.wait(100)
                        logger.info("🔊 Audio playback completed")
                    else:
                        logger.error("❌ No audio data in result")
                        return False
                return True
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logger.error(f"❌ TTS synthesis canceled: {cancellation.reason}")
                if cancellation.error_details:
                    logger.error(f"❌ TTS error details: {cancellation.error_details}")
                return False if not return_bytes else b''
            else:
                logger.error(f"❌ TTS synthesis failed with reason: {result.reason}")
                return False if not return_bytes else b''
                
        except Exception as e:
            logger.error(f"❌ TTS Exception: {e}", exc_info=True)
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
            'avg_ai_duration': sum(ai_durations) / len(ai_durations),
            'avg_tts_duration': sum(tts_durations) / len(tts_durations)
        }
    
    def print_timing_statistics(self):
        """Print comprehensive timing statistics"""
        stats = self.get_timing_statistics()
        
        if not stats:
            print("📊 No timing data available yet")
            return
        
        print("\n" + "=" * 60)
        print("📊 CONVERSATION TIMING STATISTICS")
        print("=" * 60)
        print(f"Total Conversations: {stats['total_conversations']}")
        print(f"Average Total Latency: {stats['avg_total_latency']:.2f}s")
        print(f"Best Response Time: {stats['min_total_latency']:.2f}s")
        print(f"Worst Response Time: {stats['max_total_latency']:.2f}s")
        print("-" * 60)
        print("BREAKDOWN BY COMPONENT:")
        print(f"  🎤 Speech Recognition: {stats['avg_stt_duration']:.2f}s avg")
        print(f"  🤖 AI Processing:      {stats['avg_ai_duration']:.2f}s avg")
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
            filename = f"therapy_session_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Omani Therapist AI - Session Transcript\n")
                f.write("=" * 50 + "\n")
                f.write(f"Session Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Messages: {len(self.session_memory)}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, msg in enumerate(self.session_memory, 1):
                    if msg.role != "system":  # Skip system message in transcript
                        f.write(f"[{i}] {msg.role.upper()} ({msg.timestamp.strftime('%H:%M:%S')})\n")
                        f.write(f"{msg.content}\n")
                        if msg.voice_gender or msg.emotion:
                            f.write(f"    Voice: {msg.voice_gender}, Emotion: {msg.emotion}\n")
                        f.write("\n")
                
                # Add timing statistics
                f.write("\n" + "=" * 50 + "\n")
                f.write("TIMING PERFORMANCE STATISTICS\n")
                f.write("=" * 50 + "\n")
                
                stats = self.get_timing_statistics()
                if stats:
                    f.write(f"Total Conversations: {stats['total_conversations']}\n")
                    f.write(f"Average Total Latency: {stats['avg_total_latency']:.2f}s\n")
                    f.write(f"Best Response Time: {stats['min_total_latency']:.2f}s\n")
                    f.write(f"Worst Response Time: {stats['max_total_latency']:.2f}s\n")
                    f.write(f"Average STT Duration: {stats['avg_stt_duration']:.2f}s\n")
                    f.write(f"Average AI Duration: {stats['avg_ai_duration']:.2f}s\n")
                    f.write(f"Average TTS Duration: {stats['avg_tts_duration']:.2f}s\n")
                else:
                    f.write("No timing data available\n")
            
            logger.info(f"Session transcript saved to: {filename}")
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
        logger.info("Session reset")
    
    def run_conversation_loop(self):
        """
        Main conversation loop with timing measurements
        """
        print("🇴🇲 Omani Therapist AI - Conversation Started")
        print("=" * 60)
        print("🎤 Speak in Arabic to begin conversation")
        print("🔊 The AI will respond in Omani Arabic")
        print("💬 Say 'انتهى' or 'exit' to end the session")
        print("🔄 Say 'بداية جديدة' to reset the conversation")
        print("⏱️  Performance timing will be measured and reported")
        print("=" * 60)
        
        # Welcome message
        welcome_msg = "أهلاً وسهلاً بك في جلسة العلاج النفسي. أنا هنا لمساعدتك والاستماع إليك. كيف حالك اليوم؟"
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
                    print("👋 Ending session...")
                    
                    # Print final timing statistics
                    self.print_timing_statistics()
                    
                    # Farewell message
                    farewell_msg = "شكراً لك على الجلسة. أتمنى أن تكون مفيدة. إلى اللقاء، وأتمنى لك كل الخير."
                    self.speak_text(farewell_msg, self.default_voice_gender, "calm")
                    
                    # Save transcript
                    transcript_file = self.save_session_transcript()
                    if transcript_file:
                        print(f"📄 Session transcript saved: {transcript_file}")
                    
                    break
                
                # Check for reset command
                if any(word in user_input.lower() for word in ['بداية جديدة', 'reset', 'start over']):
                    print("🔄 Resetting conversation...")
                    self.reset_session()
                    
                    reset_msg = "حسناً، لنبدأ من جديد. كيف يمكنني مساعدتك اليوم؟"
                    self.speak_text(reset_msg, self.default_voice_gender, "encouraging")
                    conversation_count = 0
                    continue
                
                # Get AI response with timing
                ai_response, detected_language = self.get_ai_response(user_input, timing_metrics)
                
                if ai_response:
                    # Speak the response with timing
                    success = self.speak_text(ai_response, self.default_voice_gender, self.default_emotion, timing_metrics, language=detected_language)
                    
                    if success:
                        conversation_count += 1
                        
                        # Add completed timing metrics to history
                        self.timing_history.append(timing_metrics)
                        
                        # Print timing report for this turn
                        timing_metrics.print_timing_report()
                        
                        print(f"✅ Conversation turn {conversation_count} completed")
                    else:
                        print("❌ Failed to speak response")
                        # Still continue the conversation
                        
                else:
                    print("🚨 Failed to get AI response")
                    # Fallback response
                    fallback_msg = "أعتذر، لم أتمكن من فهم طلبك. هل يمكنك إعادة السؤال؟"
                    self.speak_text(fallback_msg, self.default_voice_gender, "neutral")
                
                # Brief pause between turns
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n🛑 Conversation interrupted by user")
            
            # Print final timing statistics
            self.print_timing_statistics()
            
            # Save transcript
            transcript_file = self.save_session_transcript()
            if transcript_file:
                print(f"📄 Session transcript saved: {transcript_file}")
                
        except Exception as e:
            logger.error(f"Conversation loop error: {e}")
            print(f"🚨 Conversation error: {e}")
            
        finally:
            print("🏁 Conversation ended")


def main():
    """Main function to run the Omani Therapist AI"""
    print("Omani Therapist AI - Conversation System")
    print("=" * 50)
    
    # Check environment variables
    required_vars = ['AZURE_SPEECH_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set up your .env file with:")
        print("   AZURE_SPEECH_KEY=your_azure_key")
        print("   AZURE_SPEECH_REGION=uaenorth")
        print("   OPENAI_API_KEY=your_openai_key")
        print("   ANTHROPIC_API_KEY=your_anthropic_key")
        return
    
    # Optional API keys warnings
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY not set - only Claude fallback available")
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  Warning: ANTHROPIC_API_KEY not set - no fallback if OpenAI fails")
    
    try:
        # Initialize the AI system
        therapist_ai = OmaniTherapistAI()
        
        # Run the conversation loop
        therapist_ai.run_conversation_loop()
        
    except Exception as e:
        logger.error(f"System initialization error: {e}")
        print(f"🚨 Failed to initialize system: {e}")
        print("\nTroubleshooting:")
        print("1. Verify your Azure Speech Services credentials")
        print("2. Check your internet connection")
        print("3. Ensure microphone permissions are enabled")
        print("4. Install required dependencies: pip install openai anthropic azure-cognitiveservices-speech pygame python-dotenv")


if __name__ == "__main__":
    main() 