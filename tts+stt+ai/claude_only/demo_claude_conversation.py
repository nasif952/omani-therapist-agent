#!/usr/bin/env python3
"""
Demo Script for Omani Therapist AI - Claude Opus 4 Edition
==========================================================

This script demonstrates the Claude-only AI conversation system with:
1. Text-based input (for testing without microphone)
2. Voice-based input (full conversation system)
3. AI-only testing mode

Usage:
    python demo_claude_conversation.py --mode text    # Text input mode
    python demo_claude_conversation.py --mode voice   # Voice input mode
    python demo_claude_conversation.py --mode test-ai # Quick AI test mode
"""

import argparse
import sys
import os
from typing import Optional, Tuple

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from omani_therapist_ai_onlyclaude import OmaniTherapistAI_OnlyClaude, ConversationMessage, TimingMetrics
    from datetime import datetime
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Please ensure all dependencies are installed:")
    print("   pip install anthropic azure-cognitiveservices-speech pygame python-dotenv")
    sys.exit(1)


class TextBasedClaudeDemo:
    """Demo class for text-based testing with Claude Opus 4 (no microphone required)"""
    
    def __init__(self):
        """Initialize the demo"""
        try:
            self.ai = OmaniTherapistAI_OnlyClaude()
            # Override the get_user_speech method to use text input
            self.ai.get_user_speech = self._get_text_input
            print("✅ Claude Opus 4 text-based demo initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Claude AI system: {e}")
            raise
    
    def _get_text_input(self, timeout_seconds: int = 10) -> Tuple[Optional[str], Optional[TimingMetrics]]:
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
        """Run the text-based Claude demo"""
        print("🇴🇲 Omani Therapist AI - Claude Opus 4 Text Demo")
        print("=" * 60)
        print("🤖 Powered by Claude Opus 4 (claude-opus-4-20250514)")
        print("💬 Type your messages in Arabic")
        print("🔊 The AI will respond and speak in Omani Arabic")
        print("📝 Type 'exit' to quit")
        print("=" * 60)
        
        # Welcome message
        welcome_msg = "أهلاً وسهلاً بك في جلسة العلاج النفسي التجريبية مع كلود أوبوس 4. اكتب رسالتك وسأجيبك بالصوت."
        print(f"🤖 Claude: {welcome_msg}")
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
                    print(f"🤖 Claude: {ai_response}")
                    
                    # Speak the response
                    success = self.ai.speak_text(ai_response, "female", "neutral")
                    
                    if success:
                        conversation_count += 1
                        print(f"✅ Claude conversation turn {conversation_count} completed")
                    else:
                        print("❌ Failed to speak response (but conversation continues)")
                        
                else:
                    print("🚨 Failed to get Claude response")
                    fallback_msg = "أعتذر، لم أتمكن من فهم طلبك. هل يمكنك إعادة كتابة السؤال؟"
                    print(f"🤖 Claude: {fallback_msg}")
                    self.ai.speak_text(fallback_msg, "female", "neutral")
                    
        except KeyboardInterrupt:
            print("\n🛑 Demo interrupted by user")
        except Exception as e:
            print(f"🚨 Demo error: {e}")
        finally:
            # Save transcript
            transcript_file = self.ai.save_session_transcript()
            if transcript_file:
                print(f"📄 Claude session transcript saved: {transcript_file}")
            print("🏁 Claude demo ended")


def test_claude_ai_only():
    """Test Claude Opus 4 responses without TTS (for quick testing)"""
    print("🧪 Testing Claude Opus 4 Response Only (No Speech)")
    print("=" * 50)
    
    try:
        import time
        
        ai = OmaniTherapistAI_OnlyClaude()
        
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
                print(f"✅ Claude Opus 4 Response: {response}")
                # Print timing info
                timing_metrics.print_timing_report()
            else:
                print("❌ No response received")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")


def check_dependencies():
    """Check if all dependencies are available"""
    print("🔍 Checking Dependencies for Claude Edition...")
    print("-" * 40)
    
    dependencies = {
        'azure.cognitiveservices.speech': 'Azure Speech SDK',
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
        print("Install with: pip install anthropic azure-cognitiveservices-speech pygame python-dotenv")
        return False
    else:
        print("\n✅ All dependencies available!")
        return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Omani Therapist AI - Claude Opus 4 Demo")
    parser.add_argument(
        '--mode', 
        choices=['text', 'voice', 'test-ai', 'check-deps'],
        default='text',
        help='Demo mode: text (keyboard input), voice (microphone), test-ai (quick Claude test), or check-deps (check dependencies)'
    )
    
    args = parser.parse_args()
    
    # Check environment variables
    if not os.getenv('AZURE_SPEECH_KEY'):
        print("❌ Error: AZURE_SPEECH_KEY not found in environment variables")
        print("Please set up your .env file with Azure credentials")
        return
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ Error: ANTHROPIC_API_KEY not found in environment variables")
        print("Please set up your .env file with Anthropic credentials")
        return
    
    if args.mode == 'check-deps':
        check_dependencies()
        return
    
    elif args.mode == 'test-ai':
        test_claude_ai_only()
        return
    
    elif args.mode == 'text':
        print("🎮 Starting Claude Opus 4 Text-Based Demo...")
        demo = TextBasedClaudeDemo()
        demo.run_demo()
        
    elif args.mode == 'voice':
        print("🎤 Starting Claude Opus 4 Voice-Based Demo...")
        try:
            ai = OmaniTherapistAI_OnlyClaude()
            ai.run_conversation_loop()
        except Exception as e:
            print(f"❌ Claude voice demo failed: {e}")
            print("Try text mode instead: python demo_claude_conversation.py --mode text")
    
    else:
        print("❌ Invalid mode specified")


if __name__ == "__main__":
    main() 