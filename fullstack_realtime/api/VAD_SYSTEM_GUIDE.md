# Voice Activity Detection (VAD) System

## Overview

The Voice Activity Detection (VAD) system provides intelligent turn detection for natural conversations, allowing users to speak continuously without interruption while the system determines when they have finished speaking.

## Key Features

### 🎯 **Smart Turn Detection**
- Accumulates speech segments over time
- Uses configurable silence timeout to determine conversation turns
- Handles natural pauses without premature processing
- Combines multiple speech segments into complete conversation turns

### ⚙️ **Configurable Parameters**
- **Silence Timeout**: How long to wait after speech ends before processing (default: 3.0s)
- **Minimum Speech Duration**: Ignore very short utterances (default: 0.5s)
- **Maximum Turn Duration**: Force processing after this time (default: 60.0s)
- **Debug Logging**: Enable detailed logging for VAD events

### 📊 **Real-time Statistics**
- Total turns processed
- Average turn length
- Total speech duration
- Current turn status

## How It Works

### 1. Speech Collection
```
User speaks: "So this is going to be very difficult situation for me"
[pause 0.5s]
User continues: "because this is a very difficult scenario"
[pause 0.8s]  
User continues: "right now cause I am building my gain"
[silence 3.0s] → TURN COMPLETE
```

### 2. Turn Processing
The system combines all segments into one complete turn:
```
Complete Turn: "So this is going to be very difficult situation for me because this is a very difficult scenario right now cause I am building my gain"
```

### 3. AI Processing
Only when a complete turn is detected, the system:
- Sends the complete text to the AI
- Detects language (English/Arabic)
- Generates appropriate response
- Uses correct TTS voice

## WebSocket Integration

### Message Types

#### Incoming (from client):
- **Audio bytes**: Raw audio data for speech recognition
- **Text commands**: JSON commands for VAD control

#### Outgoing (to client):
- `partial_transcript`: Real-time speech recognition feedback
- `final_transcript`: Finalized speech segment
- `turn_complete`: Complete conversation turn ready for processing
- `ai_response`: AI-generated response
- `tts_start`/`tts_audio`/`tts_end`: TTS audio streaming
- `vad_stats`: VAD statistics
- `error`: Error messages

### Example WebSocket Commands

#### Force Complete Turn
```json
{
  "type": "force_complete_turn"
}
```

#### Get VAD Statistics
```json
{
  "type": "get_vad_stats"
}
```

#### Update VAD Configuration
```json
{
  "type": "update_vad_config",
  "config": {
    "silence_timeout": 4.0,
    "min_speech_duration": 0.3
  }
}
```

## REST API Endpoints

### GET /api/vad/config
Get current VAD configuration and parameter descriptions.

**Response:**
```json
{
  "default_config": {
    "silence_timeout": 3.0,
    "min_speech_duration": 0.5,
    "max_turn_duration": 60.0,
    "word_pause_threshold": 1.0,
    "debug_logging": true
  },
  "description": {
    "silence_timeout": "Seconds to wait after speech ends before processing turn",
    "min_speech_duration": "Minimum speech duration to consider valid turn",
    "max_turn_duration": "Maximum turn duration before forcing processing",
    "word_pause_threshold": "Minimum silence between words (not used currently)",
    "debug_logging": "Enable detailed logging for VAD events"
  }
}
```

## Configuration Guidelines

### For Different Use Cases

#### **Quick Conversations** (shorter timeout)
```python
VADConfig(
    silence_timeout=1.5,
    min_speech_duration=0.3,
    max_turn_duration=30.0
)
```

#### **Thoughtful Conversations** (longer timeout)
```python
VADConfig(
    silence_timeout=4.0,
    min_speech_duration=0.8,
    max_turn_duration=90.0
)
```

#### **Presentation Mode** (very long timeout)
```python
VADConfig(
    silence_timeout=6.0,
    min_speech_duration=1.0,
    max_turn_duration=300.0
)
```

## Benefits

### ✅ **Natural Conversation Flow**
- Users can speak naturally with pauses
- No need to worry about premature interruption
- System waits for complete thoughts

### ✅ **Better AI Responses**
- AI receives complete context
- More coherent and relevant responses
- Better language detection accuracy

### ✅ **Improved User Experience**
- Real-time feedback during speech
- Clear indication when turn is complete
- Configurable for different speaking styles

### ✅ **Robust Error Handling**
- Handles network interruptions
- Graceful fallback mechanisms
- Detailed logging for debugging

## Example Usage Scenario

**User Input:**
```
"So this is going to be very difficult situation for me because this is a very difficult scenario right now cause I am building my gain and sometimes it's falling up. So I have a lot of things to do, but sometimes it is hard to track out of. So I would like to help you our consideration so in my problems so that you can actually help me. And I would like to have to have some guidelines so that I can follow every day. So there are certain things I need to focus on. First of all, focus on my carries the my prime volume, then my study."
```

**System Behavior:**
1. Collects speech segments in real-time
2. Provides partial transcripts for feedback
3. Waits for 3-second silence
4. Combines all segments into complete turn
5. Processes with AI for comprehensive response
6. Generates appropriate TTS with correct language

## Troubleshooting

### Common Issues

#### **Turns Complete Too Early**
- Increase `silence_timeout` (e.g., 4.0s)
- Check for background noise causing false speech detection

#### **Turns Take Too Long**
- Decrease `silence_timeout` (e.g., 2.0s)
- Reduce `max_turn_duration` for faster processing

#### **Short Utterances Ignored**
- Decrease `min_speech_duration` (e.g., 0.3s)
- Check microphone sensitivity

#### **System Unresponsive**
- Use force completion command
- Check WebSocket connection
- Review logs for errors

## Technical Implementation

### Core Components

1. **VoiceActivityDetector**: Main VAD logic
2. **VADConfig**: Configuration management
3. **SpeechSegment**: Individual speech segment representation
4. **WebSocket Integration**: Real-time communication
5. **Async Callback System**: Turn completion handling

### Performance Considerations

- Efficient speech segment accumulation
- Minimal memory footprint
- Optimized for real-time processing
- Scalable for multiple concurrent users

## Future Enhancements

- Adaptive timeout based on speaking patterns
- Emotion detection integration
- Multi-language VAD optimization
- Advanced noise filtering
- Speaker identification support 