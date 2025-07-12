#!/usr/bin/env python3
"""
Azure Text-to-Speech Test for Omani Arabic
==========================================

This script tests Azure's native Omani Arabic voices:
- ar-OM-AbdullahNeural (Male)
- ar-OM-AyshaNeural (Female)

Requirements:
- Azure Speech Services subscription
- azure-cognitiveservices-speech package
"""

import azure.cognitiveservices.speech as speechsdk
import os
import time
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv(dotenv_path='../../.env')  # Look for .env in project root
load_dotenv()  # Also check current directory as fallback


class AzureOmaniTTSTest:
    def __init__(self, speech_key=None, service_region=None):
        """
        Initialize Azure TTS Test
        
        Args:
            speech_key: Azure Speech Services key (or set AZURE_SPEECH_KEY env var)
            service_region: Azure region (or set AZURE_SPEECH_REGION env var)
        """
        # Try to load from environment variables first
        self.speech_key = speech_key or os.getenv('AZURE_SPEECH_KEY')
        self.service_region = service_region or os.getenv('AZURE_SPEECH_REGION', 'uaenorth')
        
        # If still no key, try backup key
        if not self.speech_key:
            self.speech_key = os.getenv('AZURE_SPEECH_KEY_BACKUP')
        
        if not self.speech_key:
            raise ValueError("Please provide speech_key or set AZURE_SPEECH_KEY environment variable")
        
        # Omani Arabic voices
        self.omani_voices = {
            'male': 'ar-OM-AbdullahNeural',
            'female': 'ar-OM-AyshaNeural'
        }
        
        # Test texts for evaluation
        self.test_texts = {
            'greeting': "مرحبا، كيف حالك اليوم؟ أتمنى أن تكون بخير.",
            'therapy_intro': "أهلاً وسهلاً بك. أنا هنا لمساعدتك والاستماع إليك. كيف تشعر اليوم؟",
            'omani_specific': "يا أهلا وسهلا فيك في عمان الحبيبة. شلونك؟ إن شاء الله تمام.",
            'medical_terms': "سأقوم بفحص ضغط الدم ونبضات القلب. يرجى أخذ نفس عميق والاسترخاء.",
            'emotional_support': "أفهم مشاعرك وأقدر ثقتك بي. دعنا نتحدث عما يقلقك.",
            'numbers_dates': "موعدك القادم يوم الاثنين الساعة الثانية والنصف بعد الظهر.",
            'complex_sentence': "العلاج النفسي عملية تستغرق وقتاً وصبراً، ولكن النتائج ستكون مفيدة جداً لصحتك النفسية."
        }
        
        # Create output directory
        self.output_dir = "omani_tts_samples"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def configure_speech_service(self, voice_name):
        """Configure Azure Speech Service with specific voice"""
        speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, 
            region=self.service_region
        )
        speech_config.speech_synthesis_voice_name = voice_name
        
        # Configure audio format for HIGHEST quality (48kHz uncompressed)
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm
        )
        
        return speech_config
    
    def synthesize_text(self, text, voice_name, output_filename):
        """Synthesize text to speech and save as audio file"""
        try:
            speech_config = self.configure_speech_service(voice_name)
            
            # Create audio config for file output
            audio_config = speechsdk.audio.AudioOutputConfig(
                filename=os.path.join(self.output_dir, output_filename)
            )
            
            # Create synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            print(f"Synthesizing with {voice_name}: {text[:50]}...")
            
            # Synthesize speech
            result = synthesizer.speak_text_async(text).get()
            
            if result and result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print(f"✅ Success: Audio saved to {output_filename}")
                return True
            else:
                error_reason = result.reason if result else "Unknown error"
                print(f"❌ Error: {error_reason}")
                if result and result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    if cancellation_details:
                        print(f"Error details: {cancellation_details.reason}")
                        if hasattr(cancellation_details, 'error_details') and cancellation_details.error_details:
                            print(f"Error message: {cancellation_details.error_details}")
                return False
                
        except Exception as e:
            print(f"❌ Exception occurred: {e}")
            return False
    
    def test_with_ssml(self, voice_name, gender):
        """Test with SSML for advanced speech control"""
        ssml_text = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ar-OM">
            <voice name="{voice_name}">
                <prosody rate="medium" pitch="medium" volume="medium">
                    <emphasis level="moderate">مرحباً بك في جلسة العلاج النفسي.</emphasis>
                </prosody>
                <break time="1s"/>
                <prosody rate="slow" pitch="low" volume="soft">
                    <emphasis level="reduced">دعنا نبدأ بهدوء وتركيز.</emphasis>
                </prosody>
                <break time="500ms"/>
                <prosody rate="medium" pitch="medium" volume="medium">
                    <emphasis level="strong">كيف تشعر اليوم؟</emphasis>
                </prosody>
            </voice>
        </speak>
        """
        
        try:
            speech_config = self.configure_speech_service(voice_name)
            
            output_filename = f"ssml_test_{gender}_omani.wav"  # WAV for highest quality
            audio_config = speechsdk.audio.AudioOutputConfig(
                filename=os.path.join(self.output_dir, output_filename)
            )
            
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            print(f"Testing SSML with {voice_name}...")
            result = synthesizer.speak_ssml_async(ssml_text).get()
            
            if result and result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print(f"✅ SSML Success: Audio saved to {output_filename}")
                return True
            else:
                error_reason = result.reason if result else "Unknown error"
                print(f"❌ SSML Error: {error_reason}")
                return False
                
        except Exception as e:
            print(f"❌ SSML Exception: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run comprehensive test of both Omani voices"""
        print("🇴🇲 Starting Azure Omani Arabic TTS Comprehensive Test")
        print("=" * 60)
        key_display = '****' if not self.speech_key or len(self.speech_key) <= 4 else f"{'*' * 10}{self.speech_key[-4:]}"
        print(f"Speech Key: {key_display}")
        print(f"Region: {self.service_region}")
        print(f"Output Directory: {self.output_dir}")
        print("=" * 60)
        
        test_results = {
            'timestamp': datetime.now().isoformat(),
            'region': self.service_region,
            'voices_tested': [],
            'successful_tests': 0,
            'failed_tests': 0
        }
        
        # Test both voices with all test texts
        for gender, voice_name in self.omani_voices.items():
            print(f"\n🎤 Testing {gender.upper()} voice: {voice_name}")
            print("-" * 40)
            
            voice_results = {
                'voice_name': voice_name,
                'gender': gender,
                'test_results': {}
            }
            
            for test_name, text in self.test_texts.items():
                output_filename = f"{test_name}_{gender}_omani.wav"  # WAV for highest quality
                success = self.synthesize_text(text, voice_name, output_filename)
                
                voice_results['test_results'][test_name] = {
                    'success': success,
                    'text': text,
                    'output_file': output_filename
                }
                
                if success:
                    test_results['successful_tests'] += 1
                else:
                    test_results['failed_tests'] += 1
                
                time.sleep(0.5)  # Small delay between requests
            
            # Test SSML capabilities
            print(f"\n🔧 Testing SSML with {gender} voice...")
            ssml_success = self.test_with_ssml(voice_name, gender)
            voice_results['ssml_test'] = ssml_success
            
            test_results['voices_tested'].append(voice_results)
        
        # Save test results
        results_file = os.path.join(self.output_dir, "test_results.json")
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, ensure_ascii=False, indent=2)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Successful tests: {test_results['successful_tests']}")
        print(f"❌ Failed tests: {test_results['failed_tests']}")
        print(f"📁 Audio files saved in: {self.output_dir}")
        print(f"📋 Test results saved in: {results_file}")
        
        # Evaluation instructions
        print("\n🎧 EVALUATION INSTRUCTIONS:")
        print("-" * 30)
        print("1. Listen to each audio file in the output directory")
        print("2. Compare male vs female voices for naturalness")
        print("3. Pay attention to:")
        print("   • Pronunciation of Omani-specific terms")
        print("   • Natural rhythm and intonation")
        print("   • Emotional expressiveness")
        print("   • Medical/therapy terminology accuracy")
        print("4. Test the SSML files for advanced speech control")
        
        return test_results


def main():
    """Main function to run the test"""
    print("Azure Omani Arabic TTS Testing Tool")
    print("Using environment variables for secure credential management.\n")
    
    # Get credentials from environment variables
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    service_region = os.getenv('AZURE_SPEECH_REGION', 'uaenorth')
    
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
    
    print(f"🔑 Using key ending in: ...{speech_key[-4:]}")
    print(f"🌍 Region: {service_region}")
    print("(Loaded from environment variables)")
    
    try:
        # Initialize and run test
        tts_test = AzureOmaniTTSTest(speech_key=speech_key, service_region=service_region)
        results = tts_test.run_comprehensive_test()
        
        print(f"\n🎉 Test completed! Check the '{tts_test.output_dir}' folder for audio samples.")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify your Azure Speech Key is correct")
        print("2. Check your internet connection")
        print("3. Ensure your Azure subscription is active")
        print("4. Try a different Azure region")


if __name__ == "__main__":
    main() 