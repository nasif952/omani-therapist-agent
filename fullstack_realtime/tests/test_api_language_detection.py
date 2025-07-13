#!/usr/bin/env python3
"""
Test script for API language detection functionality
"""

import requests
import json
import time

def test_api_language_detection():
    """Test API endpoints with different languages"""
    print("Testing API Language Detection")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test cases with different languages
    test_cases = [
        {
            "text": "Hello, I am feeling anxious today. Can you help me?",
            "expected_language": "en",
            "description": "English anxiety question"
        },
        {
            "text": "مرحبا، أشعر بالقلق اليوم. هل يمكنك مساعدتي؟",
            "expected_language": "ar", 
            "description": "Arabic anxiety question"
        },
        {
            "text": "I need someone to talk to about my depression",
            "expected_language": "en",
            "description": "English depression statement"
        },
        {
            "text": "أحتاج إلى شخص للتحدث معه حول الاكتئاب",
            "expected_language": "ar",
            "description": "Arabic depression statement"
        }
    ]
    
    print(f"Testing {len(test_cases)} cases...")
    print("-" * 30)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Input: {test_case['text']}")
        
        try:
            # Test the /api/text endpoint
            response = requests.post(
                f"{base_url}/api/text",
                data={"text": test_case['text']},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if "error" in data:
                    print(f"❌ API Error: {data['error']}")
                    continue
                
                # Check if we got a response
                if "ai_response" in data:
                    ai_response = data["ai_response"]
                    print(f"✅ AI Response: {ai_response[:100]}...")
                    
                    # Check if TTS audio was generated
                    if "tts_audio_base64" in data and data["tts_audio_base64"]:
                        print(f"✅ TTS Audio generated (size: {len(data['tts_audio_base64'])} chars)")
                    else:
                        print("❌ No TTS audio generated")
                    
                    # Check crisis detection
                    if "is_crisis_detected" in data:
                        crisis_status = "🚨 Crisis detected" if data["is_crisis_detected"] else "✅ No crisis"
                        print(f"Crisis Detection: {crisis_status}")
                    
                else:
                    print("❌ No AI response received")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        # Small delay between requests
        time.sleep(2)
    
    print("\n" + "=" * 50)
    print("API Language Detection Test Complete")

def test_health_endpoint():
    """Test the health endpoint"""
    print("\nTesting Health Endpoint")
    print("-" * 30)
    
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def main():
    """Run all API tests"""
    print("API Language Detection Tests")
    print("=" * 60)
    
    # First check if server is running
    if not test_health_endpoint():
        print("❌ Server is not running. Please start the server first.")
        print("Run: cd api && python main.py")
        return False
    
    # Run language detection tests
    test_api_language_detection()
    
    print("\n🎉 API testing complete!")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 