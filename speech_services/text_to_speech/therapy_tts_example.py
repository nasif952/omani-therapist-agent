#!/usr/bin/env python3
"""
Therapy Application TTS Integration Example
==========================================

This example shows how to integrate Azure Omani Arabic TTS 
into a therapy/healthcare application.

Features:
- Dynamic voice selection (male/female)
- Therapy-specific text templates
- Emotional tone control with SSML
- Real-time audio playback
- Session audio logging
"""

import azure.cognitiveservices.speech as speechsdk
import os
import io
import pygame
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv(dotenv_path='../../.env')  # Look for .env in project root
load_dotenv()  # Also check current directory as fallback


class TherapyTTSService:
    def __init__(self, speech_key: str, region: str = "uaenorth"):
        """Initialize Therapy TTS Service"""
        self.speech_key = speech_key
        self.region = region
        
        # Configure speech service
        self.speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=region
        )
        
        # Set HIGHEST quality audio format (48kHz uncompressed)
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm
        )
        
        # Available Omani voices
        self.voices = {
            'male': 'ar-OM-AbdullahNeural',
            'female': 'ar-OM-AyshaNeural'
        }
        
        # Initialize pygame for HIGHEST quality audio playback (48kHz)
        pygame.mixer.init(frequency=48000, size=-16, channels=1, buffer=1024)
        
        # Therapy text templates
        self.therapy_templates = {
            'session_start': {
                'formal': "أهلاً وسهلاً بك في جلسة العلاج النفسي. أنا هنا لمساعدتك والاستماع إليك.",
                'casual': "مرحبا! كيف حالك اليوم؟ أتمنى أن تكون بخير.",
                'omani': "يا أهلا وسهلا فيك! شلونك اليوم؟ إن شاء الله تمام."
            },
            'encouragement': {
                'support': "أفهم مشاعرك وأقدر ثقتك بي. سنتخطى هذا معاً.",
                'progress': "أرى تقدماً واضحاً في حالتك. استمر على هذا النهج الإيجابي.",
                'strength': "لديك القوة والشجاعة لتجاوز هذه التحديات."
            },
            'breathing_exercise': {
                'start': "دعنا نبدأ بتمرين التنفس. اتبع صوتي بهدوء.",
                'inhale': "خذ نفساً عميقاً... واحد... اثنان... ثلاثة... أربعة...",
                'hold': "احبس النفس... واحد... اثنان... ثلاثة... أربعة...",
                'exhale': "أخرج النفس ببطء... واحد... اثنان... ثلاثة... أربعة..."
            },
            'session_end': {
                'summary': "لقد كانت جلسة مفيدة جداً. أشكرك على انفتاحك وثقتك.",
                'homework': "أتذكر أن تمارس التقنيات التي تعلمتها اليوم.",
                'next_appointment': "موعدنا القادم سيكون مفيداً أكثر. إلى اللقاء."
            }
        }
    
    def create_ssml_text(self, text: str, emotion: str = "neutral", 
                        rate: str = "medium", pitch: str = "medium", 
                        voice_name: Optional[str] = None) -> str:
        """Create SSML formatted text with emotional control"""
        if not voice_name:
            voice_name = self.voices['female']  # Default to female voice
        
        # Emotion-specific prosody settings
        emotion_settings = {
            'calm': {'rate': 'slow', 'pitch': 'low'},
            'encouraging': {'rate': 'medium', 'pitch': 'medium'},
            'excited': {'rate': 'fast', 'pitch': 'high'},
            'sad': {'rate': 'x-slow', 'pitch': 'x-low'},
            'neutral': {'rate': rate, 'pitch': pitch}
        }
        
        settings = emotion_settings.get(emotion, emotion_settings['neutral'])
        
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ar-OM">
            <voice name="{voice_name}">
                <prosody rate="{settings['rate']}" pitch="{settings['pitch']}" volume="medium">
                    <emphasis level="moderate">{text}</emphasis>
                </prosody>
            </voice>
        </speak>
        """
        
        return ssml.strip()
    
    def speak_text(self, text: str, voice_gender: str = "female", 
                   emotion: str = "neutral", play_audio: bool = True,
                   save_to_file: Optional[str] = None) -> bool:
        """
        Convert text to speech and optionally play or save
        
        Args:
            text: Arabic text to synthesize
            voice_gender: 'male' or 'female'
            emotion: 'calm', 'encouraging', 'excited', 'sad', 'neutral'
            play_audio: Whether to play audio immediately
            save_to_file: Optional filename to save audio
        """
        try:
            voice_name = self.voices.get(voice_gender, self.voices['female'])
            self.speech_config.speech_synthesis_voice_name = voice_name
            
            # Create SSML text with emotional control
            ssml_text = self.create_ssml_text(text, emotion, voice_name=voice_name)
            
            if save_to_file:
                # Save to file
                audio_config = speechsdk.audio.AudioOutputConfig(filename=save_to_file)
                synthesizer = speechsdk.SpeechSynthesizer(
                    speech_config=self.speech_config,
                    audio_config=audio_config
                )
                result = synthesizer.speak_ssml_async(ssml_text).get()
            else:
                # Synthesize to memory for immediate playback
                synthesizer = speechsdk.SpeechSynthesizer(
                    speech_config=self.speech_config,
                    audio_config=None
                )
                result = synthesizer.speak_ssml_async(ssml_text).get()
            
            if result and result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                if play_audio and not save_to_file and result.audio_data:
                    # Play audio using pygame
                    audio_stream = io.BytesIO(result.audio_data)
                    pygame.mixer.music.load(audio_stream)
                    pygame.mixer.music.play()
                    
                    # Wait for playback to complete
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
                
                return True
            else:
                print(f"TTS Error: {result.reason if result else 'Unknown error'}")
                return False
                
        except Exception as e:
            print(f"TTS Exception: {e}")
            return False
    
    def therapy_session_demo(self, voice_gender: str = "female", 
                           save_session: bool = False) -> None:
        """Demo of a complete therapy session with different emotional tones"""
        
        print(f"🎭 Starting Therapy Session Demo with {voice_gender} voice")
        print("=" * 50)
        
        session_dir = None
        if save_session:
            session_dir = f"therapy_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(session_dir, exist_ok=True)
            print(f"📁 Session audio will be saved to: {session_dir}")
        
        # Session start - welcoming tone
        print("🔊 Session Start (Welcoming)")
        start_text = self.therapy_templates['session_start']['omani']
        save_file = f"{session_dir}/01_session_start.wav" if save_session else None
        self.speak_text(start_text, voice_gender, "encouraging", True, save_file)
        
        input("Press Enter to continue...")
        
        # Breathing exercise - calm tone
        print("🔊 Breathing Exercise (Calm)")
        breathing_texts = [
            self.therapy_templates['breathing_exercise']['start'],
            self.therapy_templates['breathing_exercise']['inhale'],
            self.therapy_templates['breathing_exercise']['hold'],
            self.therapy_templates['breathing_exercise']['exhale']
        ]
        
        for i, breath_text in enumerate(breathing_texts):
            save_file = f"{session_dir}/02_breathing_{i+1}.wav" if save_session else None
            self.speak_text(breath_text, voice_gender, "calm", True, save_file)
            if i < len(breathing_texts) - 1:
                input("Press Enter for next breathing step...")
        
        input("Press Enter to continue...")
        
        # Encouragement - supportive tone
        print("🔊 Encouragement (Supportive)")
        encourage_text = self.therapy_templates['encouragement']['support']
        save_file = f"{session_dir}/03_encouragement.wav" if save_session else None
        self.speak_text(encourage_text, voice_gender, "encouraging", True, save_file)
        
        input("Press Enter to continue...")
        
        # Progress acknowledgment - positive tone
        print("🔊 Progress Acknowledgment (Positive)")
        progress_text = self.therapy_templates['encouragement']['progress']
        save_file = f"{session_dir}/04_progress.wav" if save_session else None
        self.speak_text(progress_text, voice_gender, "excited", True, save_file)
        
        input("Press Enter to continue...")
        
        # Session end - formal closing
        print("🔊 Session End (Professional)")
        end_text = self.therapy_templates['session_end']['summary']
        save_file = f"{session_dir}/05_session_end.wav" if save_session else None
        self.speak_text(end_text, voice_gender, "neutral", True, save_file)
        
        print("\n✅ Therapy session demo completed!")
        if save_session:
            print(f"📁 All audio files saved in: {session_dir}")
    
    def interactive_test(self):
        """Interactive testing interface"""
        print("🎤 Interactive Therapy TTS Test")
        print("=" * 40)
        
        while True:
            print("\nAvailable options:")
            print("1. Test with custom text")
            print("2. Use therapy templates")
            print("3. Run full session demo")
            print("4. Exit")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                text = input("Enter Arabic text: ").strip()
                if text:
                    gender = input("Voice gender (male/female) [female]: ").strip() or "female"
                    emotion = input("Emotion (calm/encouraging/excited/sad/neutral) [neutral]: ").strip() or "neutral"
                    save = input("Save to file? (y/n) [n]: ").strip().lower() == 'y'
                    
                    save_file = None
                    if save:
                        filename = input("Filename (without extension): ").strip()
                        save_file = f"{filename}.wav" if filename else "custom_test.wav"  # WAV for highest quality
                    
                    self.speak_text(text, gender, emotion, True, save_file)
            
            elif choice == "2":
                print("\nTherapy Templates:")
                for category, templates in self.therapy_templates.items():
                    print(f"{category}:")
                    for key in templates.keys():
                        print(f"  - {key}")
                
                category = input("\nSelect category: ").strip()
                if category in self.therapy_templates:
                    template_key = input(f"Select template from {category}: ").strip()
                    if template_key in self.therapy_templates[category]:
                        text = self.therapy_templates[category][template_key]
                        gender = input("Voice gender (male/female) [female]: ").strip() or "female"
                        emotion = input("Emotion [neutral]: ").strip() or "neutral"
                        self.speak_text(text, gender, emotion)
            
            elif choice == "3":
                gender = input("Session voice gender (male/female) [female]: ").strip() or "female"
                save = input("Save session audio? (y/n) [n]: ").strip().lower() == 'y'
                self.therapy_session_demo(gender, save)
            
            elif choice == "4":
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid option. Please try again.")


def main():
    """Main function"""
    print("Therapy TTS Integration Example")
    print("===============================")
    
    # Get credentials from environment variables
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    region = os.getenv('AZURE_SPEECH_REGION', 'uaenorth')
    
    # Try backup key if primary not found
    if not speech_key:
        speech_key = os.getenv('AZURE_SPEECH_KEY_BACKUP')
    
    if not speech_key:
        print("❌ Error: Azure Speech Key not found!")
        print("\nPlease set up your environment variables:")
        print("1. Copy the template: cp .env.example .env")
        print("2. Edit .env with your Azure credentials")
        print("3. Run the script again")
        print("\nAlternatively, set environment variables directly:")
        print("   export AZURE_SPEECH_KEY=your_key_here")
        print("   export AZURE_SPEECH_REGION=uaenorth")
        return
    
    print(f"🔑 Using credentials ending in: ...{speech_key[-4:]}")
    print(f"🌍 Region: {region}")
    print("(Loaded from environment variables)")
    
    try:
        # Initialize TTS service
        tts_service = TherapyTTSService(speech_key, region)
        
        # Run interactive test
        tts_service.interactive_test()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Valid Azure Speech Services credentials")
        print("2. Internet connection")
        print("3. Required dependencies installed (pygame, azure-cognitiveservices-speech)")


if __name__ == "__main__":
    main() 