import React, { useState, useRef, useEffect } from 'react';

interface VoiceModeProps {
  onCrisisDetected: (detected: boolean) => void;
}

interface ConversationTurn {
  userText: string;
  aiResponse: string;
  timestamp: number;
  isCrisis: boolean;
}

const API_BASE = '/api';

const VoiceMode: React.FC<VoiceModeProps> = ({ onCrisisDetected }) => {
  // Voice recording state
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState<string | null>(null);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [status, setStatus] = useState('Ready to record');
  
  // Conversation state
  const [currentUserText, setCurrentUserText] = useState('');
  const [currentAiResponse, setCurrentAiResponse] = useState('');
  const [conversationHistory, setConversationHistory] = useState<ConversationTurn[]>([]);
  const [ttsAudioURL, setTtsAudioURL] = useState<string | null>(null);
  const [isPlayingTTS, setIsPlayingTTS] = useState(false);
  
  // Refs
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Helper function to convert base64 to blob
  const b64toBlob = (b64Data: string, contentType = 'audio/wav', sliceSize = 512) => {
    const byteCharacters = atob(b64Data);
    const byteArrays = [];
    for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
      const slice = byteCharacters.slice(offset, offset + sliceSize);
      const byteNumbers = new Array(slice.length);
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      byteArrays.push(byteArray);
    }
    return new Blob(byteArrays, { type: contentType });
  };

  const startRecording = async () => {
    setStatus('🎤 Requesting microphone access...');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/wav';
      
      const mediaRecorder = new MediaRecorder(stream, { mimeType });
      mediaRecorderRef.current = mediaRecorder;
      audioChunks.current = [];
      
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunks.current.push(e.data);
      };
      
      mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunks.current, { type: mimeType });
        setAudioBlob(blob);
        setAudioURL(URL.createObjectURL(blob));
      };
      
      mediaRecorder.start();
      setRecording(true);
      setStatus('🎤 Recording... Speak naturally in Arabic or English');
    } catch (err) {
      setStatus('❌ Microphone access denied. Please allow microphone access.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream?.getTracks().forEach(track => track.stop());
      setRecording(false);
      setStatus('✅ Recording complete. Click "Send Audio" to process.');
    }
  };

  const processAudio = async () => {
    if (!audioBlob) return;

    setIsProcessing(true);
    setStatus('🔄 Processing audio...');
    setCurrentUserText('');
    setCurrentAiResponse('');
    setTtsAudioURL(null);

    try {
      const formData = new FormData();
      formData.append('file', audioBlob, 'audio.wav');

      const response = await fetch(`${API_BASE}/audio`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        setStatus(`❌ ${data.error}`);
        return;
      }

      const userText = data.recognized_text || data.user_text || '';
      const aiResponse = data.ai_response || '';
      const isCrisis = data.is_crisis_detected || false;

      setCurrentUserText(userText);
      setCurrentAiResponse(aiResponse);
      onCrisisDetected(isCrisis);

      // Add to conversation history
      if (userText && aiResponse) {
        const newTurn: ConversationTurn = {
          userText,
          aiResponse,
          timestamp: data.timestamp || Date.now(),
          isCrisis
        };
        setConversationHistory(prev => [...prev, newTurn]);
      }

      // Handle TTS audio
      if (data.tts_audio_base64) {
        const audioBlob = b64toBlob(data.tts_audio_base64, 'audio/wav');
        const audioURL = URL.createObjectURL(audioBlob);
        setTtsAudioURL(audioURL);
      }

      setStatus(isCrisis 
        ? '🚨 Crisis detected - Professional help recommended' 
        : '✅ Audio processed successfully');

      // Clear audio for next recording
      setAudioURL(null);
      setAudioBlob(null);
        
    } catch (error) {
      setStatus('❌ Error processing audio. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const playTTSAudio = (audioURL?: string) => {
    const urlToPlay = audioURL || ttsAudioURL;
    if (!urlToPlay) return;

    if (audioRef.current) {
      audioRef.current.pause();
    }

    const audio = new Audio(urlToPlay);
    audioRef.current = audio;
    
    audio.onplay = () => setIsPlayingTTS(true);
    audio.onended = () => setIsPlayingTTS(false);
    audio.onerror = () => setIsPlayingTTS(false);
    
    audio.play().catch(() => setIsPlayingTTS(false));
  };

  return (
    <div className="voice-mode">
      {/* Status Bar */}
      <div className="voice-status">
        <div className="status-content">
          <div className="status-icon">
            {recording ? '🎤' : isProcessing ? '🔄' : '✅'}
          </div>
          <span className="status-text">{status}</span>
        </div>
      </div>

      {/* Recording Section */}
      <div className="recording-section">
        <div className="recording-card">
          <div className="recording-header">
            <h3>Voice Recording</h3>
            <p>Speak naturally in Arabic or English</p>
          </div>
          
          <div className="recording-controls">
            <div className="record-area">
              <button 
                className={`record-button ${recording ? 'recording' : ''}`}
                onClick={recording ? stopRecording : startRecording}
                disabled={isProcessing}
              >
                <div className="record-visual">
                  <div className="record-circle">
                    <div className="record-dot"></div>
                  </div>
                  {recording && (
                    <div className="pulse-rings">
                      <div className="pulse-ring"></div>
                      <div className="pulse-ring"></div>
                      <div className="pulse-ring"></div>
                    </div>
                  )}
                </div>
                <span className="record-text">
                  {recording ? 'Stop Recording' : 'Start Recording'}
                </span>
              </button>
              
              {recording && (
                <div className="recording-timer">
                  <div className="timer-dot"></div>
                  <span>Recording...</span>
                </div>
              )}
            </div>
          </div>

          {/* Audio Preview */}
          {audioURL && (
            <div className="audio-preview">
              <div className="preview-header">
                <h4>Recording Preview</h4>
                <span className="preview-size">
                  {audioBlob ? (audioBlob.size / 1024).toFixed(1) + ' KB' : ''}
                </span>
              </div>
              <div className="audio-controls">
                <audio controls src={audioURL} className="audio-player" />
                <button 
                  className="process-button"
                  onClick={processAudio}
                  disabled={isProcessing || !audioBlob}
                >
                  <span className="button-icon">
                    {isProcessing ? '🔄' : '🚀'}
                  </span>
                  {isProcessing ? 'Processing...' : 'Send Audio'}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Current Conversation */}
      {(currentUserText || currentAiResponse) && (
        <div className="current-conversation">
          <div className="conversation-header">
            <h3>Current Conversation</h3>
            <span className="conversation-time">
              {new Date().toLocaleTimeString()}
            </span>
          </div>
          
          <div className="conversation-messages">
            {currentUserText && (
              <div className="message user-message">
                <div className="message-avatar">👤</div>
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-sender">You</span>
                    <span className="message-time">{new Date().toLocaleTimeString()}</span>
                  </div>
                  <div className="message-text">{currentUserText}</div>
                </div>
              </div>
            )}
            
            {currentAiResponse && (
              <div className="message ai-message">
                <div className="message-avatar">🇴🇲</div>
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-sender">Omani Companion</span>
                    <span className="message-time">{new Date().toLocaleTimeString()}</span>
                  </div>
                  <div className="message-text">{currentAiResponse}</div>
                  {ttsAudioURL && (
                    <div className="message-audio">
                      <button 
                        className="play-button"
                        onClick={() => playTTSAudio(ttsAudioURL)}
                        disabled={isPlayingTTS}
                      >
                        <span className="play-icon">
                          {isPlayingTTS ? '⏸️' : '🔊'}
                        </span>
                        {isPlayingTTS ? 'Playing...' : 'Play Response'}
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Conversation History */}
      {conversationHistory.length > 0 && (
        <div className="conversation-history">
          <div className="history-header">
            <h3>Session History</h3>
            <span className="history-count">
              {conversationHistory.length} conversation{conversationHistory.length !== 1 ? 's' : ''}
            </span>
          </div>
          
          <div className="history-list">
            {conversationHistory.map((turn, index) => (
              <div key={index} className={`history-item ${turn.isCrisis ? 'crisis-turn' : ''}`}>
                <div className="history-timestamp">
                  {new Date(turn.timestamp).toLocaleString()}
                  {turn.isCrisis && <span className="crisis-badge">🚨 Crisis</span>}
                </div>
                <div className="history-messages">
                  <div className="history-user">
                    <strong>You:</strong> {turn.userText}
                  </div>
                  <div className="history-ai">
                    <strong>Companion:</strong> {turn.aiResponse}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default VoiceMode; 