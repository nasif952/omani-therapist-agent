#!/usr/bin/env python3
"""
Demo Script for Omani Therapist AI
==================================

This script demonstrates the AI conversation system with both:
1. Text-based input (for testing without microphone)
2. Voice-based input (full conversation system)

Usage:
    python demo_ai_conversation.py --mode text    # Text input mode
    python demo_ai_conversation.py --mode voice   # Voice input mode
"""

import argparse
import sys
import os
from typing import Optional, Tuple

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from omani_therapist_ai import OmaniTherapistAI, ConversationMessage, TimingMetrics
    from datetime import datetime
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Please ensure all dependencies are installed:")
    print("   pip install -r requirements.txt")
    sys.exit(1)


class TextBasedDemo:
    """Demo class for text-based testing (no microphone required)"""
    
    def __init__(self):
        """Initialize the demo"""
        try:
            self.ai = OmaniTherapistAI()
            # Override the get_user_speech method to use text input
            self.ai.get_user_speech = self._get_text_input
            print("✅ Text-based demo initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize AI system: {e}")
            raise
    
    def _get_text_input(self, timeout_seconds: int = 10) -> Tuple[Optional[str], Optional['TimingMetrics']]:
        """
        Get user input as text instead of speech
        
        Args:
            timeout_seconds: Ignored in text mode
            
        Returns:
            Tuple of (user input text or None, None for timing metrics)
        """
        try:
            print("\n🎤 Enter your message in Arabic (or 'exit' to quit):")
            user_input = input("> ").strip()
            
            if not user_input:
                return None, None
                
            if user_input.lower() in ['exit', 'quit', 'bye']:
                return 'exit', None
                
            print(f"📝 You said: {user_input}")
            return user_input, None
            
        except KeyboardInterrupt:
            return 'exit', None
        except Exception as e:
            print(f"❌ Input error: {e}")
            return None, None
    
    def run_demo(self):
        """Run the text-based demo"""
        print("🇴🇲 Omani Therapist AI - Text Demo")
        print("=" * 50)
        print("💬 Type your messages in Arabic")
        print("🤖 The AI will respond and speak in Omani Arabic")
        print("📝 Type 'exit' to quit")
        print("=" * 50)
        
        # Welcome message
        welcome_msg = "أهلاً وسهلاً بك في جلسة العلاج النفسي التجريبية. اكتب رسالتك وسأجيبك بالصوت."
        print(f"🤖 AI: {welcome_msg}")
        self.ai.speak_text(welcome_msg, "female", "encouraging")
        
        conversation_count = 0
        
        try:
            while True:
                print("\n" + "-" * 40)
                
                # Get user input
                user_input, _ = self._get_text_input()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    break
                
                # Get AI response with timing metrics
                import time
                
                start_time = time.time()
                timing_metrics = TimingMetrics(
                    speech_start_time=start_time,
                    speech_end_time=start_time + 0.1,  # Simulate 0.1s speech
                    ai_processing_start_time=0,
                    ai_processing_end_time=0,
                    tts_start_time=0,
                    tts_end_time=0,
                    voice_playback_start_time=start_time + 0.1  # Set to after speech ends
                )
                
                ai_response = self.ai.get_ai_response(user_input, timing_metrics)
                
                if ai_response:
                    print(f"🤖 AI: {ai_response}")
                    
                    # Speak the response
                    success = self.ai.speak_text(ai_response, "female", "neutral")
                    
                    if success:
                        conversation_count += 1
                        print(f"✅ Conversation turn {conversation_count} completed")
                    else:
                        print("❌ Failed to speak response (but conversation continues)")
                        
                else:
                    print("🚨 Failed to get AI response")
                    fallback_msg = "أعتذر، لم أتمكن من فهم طلبك. هل يمكنك إعادة كتابة السؤال؟"
                    print(f"🤖 AI: {fallback_msg}")
                    self.ai.speak_text(fallback_msg, "female", "neutral")
                    
        except KeyboardInterrupt:
            print("\n🛑 Demo interrupted by user")
        except Exception as e:
            print(f"🚨 Demo error: {e}")
        finally:
            # Save transcript
            transcript_file = self.ai.save_session_transcript()
            if transcript_file:
                print(f"📄 Session transcript saved: {transcript_file}")
            print("🏁 Demo ended")


def test_ai_only():
    """Test AI responses without TTS (for quick testing)"""
    print("🧪 Testing AI Response Only (No Speech)")
    print("=" * 40)
    
    try:
        from omani_therapist_ai import TimingMetrics
        import time
        
        ai = OmaniTherapistAI()
        
        # Test Arabic inputs
        test_inputs = [
            "مرحبا، كيف حالك؟",
            "أشعر بالحزن اليوم",
            "هل يمكنك مساعدتي؟",
            "أريد أن أتحدث عن مشاكلي",
            "شكراً لك على المساعدة"
        ]
        
        for i, test_input in enumerate(test_inputs, 1):
            print(f"\n🧪 Test {i}: {test_input}")
            
            # Create a proper timing metrics object for testing
            start_time = time.time()
            timing_metrics = TimingMetrics(
                speech_start_time=start_time,
                speech_end_time=start_time + 0.1,  # Simulate 0.1s speech
                ai_processing_start_time=0,
                ai_processing_end_time=0,
                tts_start_time=0,
                tts_end_time=0,
                voice_playback_start_time=start_time + 0.1  # Set to after speech ends
            )
            
            response = ai.get_ai_response(test_input, timing_metrics)
            if response:
                print(f"✅ AI Response: {response}")
                # Print timing info
                timing_metrics.print_timing_report()
            else:
                print("❌ No response received")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")


def check_dependencies():
    """Check if all dependencies are available"""
    print("🔍 Checking Dependencies...")
    print("-" * 30)
    
    dependencies = {
        'azure.cognitiveservices.speech': 'Azure Speech SDK',
        'openai': 'OpenAI Python SDK',
        'anthropic': 'Anthropic Python SDK',
        'pygame': 'Pygame for audio',
        'dotenv': 'Python dotenv'
    }
    
    missing = []
    for dep, name in dependencies.items():
        try:
            __import__(dep)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} (missing)")
            missing.append(dep)
    
    if missing:
        print(f"\n🚨 Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies available!")
        return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Omani Therapist AI Demo")
    parser.add_argument(
        '--mode', 
        choices=['text', 'voice', 'test-ai', 'check-deps'],
        default='text',
        help='Demo mode: text (keyboard input), voice (microphone), test-ai (quick AI test), or check-deps (check dependencies)'
    )
    
    args = parser.parse_args()
    
    # Check environment variables
    if not os.getenv('AZURE_SPEECH_KEY'):
        print("❌ Error: AZURE_SPEECH_KEY not found in environment variables")
        print("Please set up your .env file with Azure credentials")
        return
    
    if args.mode == 'check-deps':
        check_dependencies()
        return
    
    elif args.mode == 'test-ai':
        test_ai_only()
        return
    
    elif args.mode == 'text':
        print("🎮 Starting Text-Based Demo...")
        demo = TextBasedDemo()
        demo.run_demo()
        
    elif args.mode == 'voice':
        print("🎤 Starting Voice-Based Demo...")
        try:
            ai = OmaniTherapistAI()
            ai.run_conversation_loop()
        except Exception as e:
            print(f"❌ Voice demo failed: {e}")
            print("Try text mode instead: python demo_ai_conversation.py --mode text")
    
    else:
        print("❌ Invalid mode specified")


if __name__ == "__main__":
    main() 