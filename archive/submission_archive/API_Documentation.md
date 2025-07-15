# Omani Therapist AI - API Documentation

## Overview

The Omani Therapist AI provides a RESTful API and WebSocket interface for voice-enabled mental health support in Omani Arabic dialect. The system integrates speech-to-text, AI response generation, and text-to-speech capabilities with cultural sensitivity and crisis detection.

## Base URL

```
Production: https://your-domain.vercel.app
Development: http://localhost:8000
```

## Authentication

Currently, the API does not require authentication for public endpoints. In production, implement proper authentication and rate limiting.

---

## REST API Endpoints

### 1. Health Check

**GET** `/api/health`

Check the system status and AI initialization.

**Response:**
```json
{
  "status": "ok",
  "ai_system": "initialized",
  "timestamp": 1642611234.567
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/health"
```

---

### 2. Process Audio Input

**POST** `/api/audio`

Process audio input through the complete pipeline: STT → AI → TTS

**Content-Type:** `multipart/form-data`

**Parameters:**
- `file` (required): Audio file (WAV, WebM, MP3, FLAC, M4A, OGG)

**Response:**
```json
{
  "recognized_text": "مرحبا، كيف حالك؟",
  "ai_response": "مرحبا بك! الحمد لله بخير. كيف يمكنني مساعدتك اليوم؟",
  "tts_audio_base64": "UklGRnoGAABXQVZFZm10IBAAAAABAAEA...",
  "is_crisis_detected": false,
  "timing": {
    "speech_start_time": 1642611234.567,
    "speech_end_time": 1642611235.123,
    "ai_processing_start_time": 1642611235.123,
    "ai_processing_end_time": 1642611237.456,
    "tts_start_time": 1642611237.456,
    "tts_end_time": 1642611238.789,
    "voice_playback_start_time": 1642611238.789
  },
  "timestamp": 1642611238.789
}
```

**Error Response:**
```json
{
  "error": "No speech recognized. Please try speaking clearly."
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/audio" \
  -F "file=@recording.wav"
```

**JavaScript Example:**
```javascript
const formData = new FormData();
formData.append('file', audioBlob, 'recording.webm');

const response = await fetch('/api/audio', {
  method: 'POST',
  body: formData
});

const data = await response.json();
```

---

### 3. Process Text Input

**POST** `/api/text`

Process text input through AI and TTS (bypassing STT)

**Content-Type:** `application/x-www-form-urlencoded`

**Parameters:**
- `text` (required): Text input in Arabic or English

**Response:**
```json
{
  "user_text": "أحس بقلق",
  "ai_response": "أفهم شعورك بالقلق. هذا أمر طبيعي والله يعطيك القوة...",
  "tts_audio_base64": "UklGRnoGAABXQVZFZm10IBAAAAABAAEA...",
  "is_crisis_detected": false,
  "timing": {
    "speech_start_time": 1642611234.567,
    "speech_end_time": 1642611234.567,
    "ai_processing_start_time": 1642611234.567,
    "ai_processing_end_time": 1642611237.456,
    "tts_start_time": 1642611237.456,
    "tts_end_time": 1642611238.789,
    "voice_playback_start_time": 1642611238.789
  },
  "timestamp": 1642611238.789
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=مرحبا، كيف حالك؟"
```

---

### 4. Get Session Transcript

**GET** `/api/session/transcript`

Retrieve the current session transcript and statistics.

**Response:**
```json
{
  "transcript_file": "therapy_session_20250113_143022.txt",
  "message_count": 15,
  "timing_stats": {
    "average_response_time": 3.45,
    "total_session_time": 1200.5,
    "stt_average": 1.2,
    "ai_average": 2.1,
    "tts_average": 1.1
  }
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/session/transcript"
```

---

### 5. Reset Session

**POST** `/api/session/reset`

Reset the current conversation session and clear memory.

**Response:**
```json
{
  "status": "session_reset",
  "timestamp": 1642611238.789
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/session/reset"
```

---

## WebSocket API

### Real-time Audio Streaming

**WebSocket** `/ws/audio`

Provides real-time audio streaming with live transcription and AI responses.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/audio');
```

#### Message Types

**1. Sending Audio Data**
```javascript
// Send PCM audio data (16-bit, 16kHz, mono)
const pcmData = new Int16Array(audioBuffer);
ws.send(pcmData.buffer);
```

**2. Receiving Transcription Updates**
```json
{
  "type": "partial_transcript",
  "text": "مرحبا كيف"
}
```

```json
{
  "type": "final_transcript", 
  "text": "مرحبا كيف حالك؟"
}
```

**3. Receiving AI Response**
```json
{
  "type": "ai_response",
  "text": "مرحبا بك! الحمد لله بخير. كيف يمكنني مساعدتك اليوم؟"
}
```

**4. Receiving TTS Audio**
```json
{
  "type": "tts_start"
}
```

```json
{
  "type": "tts_audio",
  "chunk": "UklGRnoGAABXQVZFZm10IBAAAAABAAEA..."
}
```

```json
{
  "type": "tts_end"
}
```

**5. Error Messages**
```json
{
  "type": "error",
  "text": "Recognition canceled: timeout"
}
```

#### Complete WebSocket Example

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/audio');
let audioChunks = [];

ws.onopen = () => {
  console.log('WebSocket connected');
  startAudioRecording();
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  switch (message.type) {
    case 'partial_transcript':
      updateTranscript(message.text, false);
      break;
      
    case 'final_transcript':
      updateTranscript(message.text, true);
      break;
      
    case 'ai_response':
      displayAIResponse(message.text);
      break;
      
    case 'tts_start':
      audioChunks = [];
      break;
      
    case 'tts_audio':
      audioChunks.push(message.chunk);
      break;
      
    case 'tts_end':
      playTTSAudio(audioChunks);
      break;
      
    case 'error':
      console.error('WebSocket error:', message.text);
      break;
  }
};

function startAudioRecording() {
  navigator.mediaDevices.getUserMedia({ 
    audio: { 
      sampleRate: 16000, 
      channelCount: 1 
    } 
  })
  .then(stream => {
    const audioContext = new AudioContext({ sampleRate: 16000 });
    const source = audioContext.createMediaStreamSource(stream);
    const processor = audioContext.createScriptProcessor(4096, 1, 1);
    
    processor.onaudioprocess = (e) => {
      const inputData = e.inputBuffer.getChannelData(0);
      const pcmData = new Int16Array(inputData.length);
      
      for (let i = 0; i < inputData.length; i++) {
        pcmData[i] = Math.max(-32768, Math.min(32767, inputData[i] * 32768));
      }
      
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(pcmData.buffer);
      }
    };
    
    source.connect(processor);
    processor.connect(audioContext.destination);
  });
}
```

---

## Crisis Detection

The system automatically detects crisis situations using pattern matching on user input.

### Crisis Indicators

The system detects various crisis patterns including:

- **Suicide ideation**: "انتحار", "اقتل نفسي", "أريد أن أموت"
- **Self-harm**: "أؤذي نفسي", "أجرح نفسي", "أعذب نفسي"
- **Hopelessness**: "مافي أمل", "تعبت من الحياة", "ما عاد أقدر"
- **Help requests**: "ساعدني", "أحتاج مساعدة عاجلة", "أنقذني"

### Crisis Response

When crisis is detected:
1. `is_crisis_detected` flag is set to `true`
2. AI receives enhanced prompting with crisis protocols
3. Response includes:
   - Immediate validation and empathy
   - Local emergency contacts (999)
   - Mental health resources
   - Islamic counseling principles
   - Professional referral encouragement

---

## Cultural Adaptation Features

### Language Support
- **Primary**: Omani Arabic dialect
- **Secondary**: Modern Standard Arabic
- **Code-switching**: Mixed Arabic-English handling

### Cultural Elements
- Islamic counseling principles
- Family-centered therapy approaches
- Gulf-specific mental health terminology
- Respect for traditional values
- Gender-sensitive responses

### Therapeutic Approaches
- Cognitive Behavioral Therapy (CBT) adapted for Arab culture
- Islamic therapy integration
- Family therapy concepts
- Community-based support emphasis

---

## Error Handling

### Common Error Responses

**400 Bad Request**
```json
{
  "error": "No file provided"
}
```

**500 Internal Server Error**
```json
{
  "error": "AI system not initialized"
}
```

**Audio Processing Errors**
```json
{
  "error": "Audio processing failed. Ensure FFmpeg is installed. Error: [details]"
}
```

**AI Service Errors**
```json
{
  "error": "AI failed to generate response. Please try again."
}
```

---

## Performance Metrics

### Timing Information

All responses include detailed timing metrics:

```json
{
  "timing": {
    "speech_start_time": 1642611234.567,
    "speech_end_time": 1642611235.123,
    "ai_processing_start_time": 1642611235.123,
    "ai_processing_end_time": 1642611237.456,
    "tts_start_time": 1642611237.456,
    "tts_end_time": 1642611238.789,
    "voice_playback_start_time": 1642611238.789
  }
}
```

### Performance Targets
- **Total Latency**: <20 seconds (end-to-end)
- **STT Processing**: <2 seconds
- **AI Response**: <15 seconds
- **TTS Synthesis**: <3 seconds

---

## Rate Limiting

**Current**: No rate limiting implemented  
**Recommended for Production**:
- 100 requests per minute per IP
- 10 concurrent WebSocket connections per IP
- 5 MB maximum audio file size

---

## Security Considerations

### Data Privacy
- Conversations are not permanently stored
- Audio data is processed in memory only
- Session transcripts are temporary files
- No personal data collection without consent

### API Security
- HTTPS required in production
- Input validation and sanitization
- File type and size restrictions
- WebSocket connection limits

---

## SDKs and Examples

### Python SDK Example

```python
import requests
import base64

class OmaniTherapistClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def process_text(self, text):
        response = requests.post(
            f"{self.base_url}/api/text",
            data={"text": text}
        )
        return response.json()
    
    def process_audio(self, audio_file_path):
        with open(audio_file_path, 'rb') as f:
            response = requests.post(
                f"{self.base_url}/api/audio",
                files={"file": f}
            )
        return response.json()
    
    def play_tts_response(self, response_data):
        if 'tts_audio_base64' in response_data:
            audio_data = base64.b64decode(response_data['tts_audio_base64'])
            # Play audio using your preferred method
            return audio_data
        return None

# Usage
client = OmaniTherapistClient()
result = client.process_text("مرحبا")
print(result['ai_response'])
```

### JavaScript/Node.js Example

```javascript
class OmaniTherapistClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }
  
  async processText(text) {
    const formData = new FormData();
    formData.append('text', text);
    
    const response = await fetch(`${this.baseUrl}/api/text`, {
      method: 'POST',
      body: formData
    });
    
    return await response.json();
  }
  
  async processAudio(audioBlob) {
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');
    
    const response = await fetch(`${this.baseUrl}/api/audio`, {
      method: 'POST',
      body: formData
    });
    
    return await response.json();
  }
  
  playTTSAudio(base64Audio) {
    const audioBlob = this.base64ToBlob(base64Audio, 'audio/wav');
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    return audio.play();
  }
  
  base64ToBlob(base64, mimeType) {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
  }
}

// Usage
const client = new OmaniTherapistClient();
client.processText('مرحبا').then(result => {
  console.log(result.ai_response);
  client.playTTSAudio(result.tts_audio_base64);
});
```

---

## Testing

### Health Check Test
```bash
curl -X GET "http://localhost:8000/api/health" | jq .
```

### Text Processing Test
```bash
curl -X POST "http://localhost:8000/api/text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=مرحبا" | jq .
```

### Crisis Detection Test
```bash
curl -X POST "http://localhost:8000/api/text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=أريد أن أموت" | jq .
```

---

## Support

For technical support or questions:
- Check the troubleshooting guide
- Review error logs in the console
- Ensure all environment variables are set
- Verify API keys are valid and have sufficient quota

---

## Changelog

### v1.0.0 (Current)
- Initial API implementation
- Basic STT/AI/TTS pipeline
- Crisis detection system
- WebSocket streaming support
- Cultural adaptation features
- Comprehensive documentation

---

*Last updated: January 2025* 