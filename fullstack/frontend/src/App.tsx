import React, { useState, useRef, useEffect } from 'react';
import './App.css';

// Types
interface ApiResponse {
  recognized_text?: string;
  user_text?: string;
  ai_response?: string;
  tts_audio_base64?: string;
  is_crisis_detected?: boolean;
  timing?: any;
  timestamp?: number;
  error?: string;
}

interface ConversationTurn {
  userText: string;
  aiResponse: string;
  timestamp: number;
  isCrisis: boolean;
}

const API_BASE = '/api';

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

const App: React.FC = () => {
  // Voice recording state
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState<string | null>(null);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  
  // Conversation state
  const [currentUserText, setCurrentUserText] = useState('');
  const [currentAiResponse, setCurrentAiResponse] = useState('');
  const [conversationHistory, setConversationHistory] = useState<ConversationTurn[]>([]);
  
  // Audio playback
  const [ttsAudioURL, setTtsAudioURL] = useState<string | null>(null);
  const [isPlayingTTS, setIsPlayingTTS] = useState(false);
  
  // UI state
  const [status, setStatus] = useState('Ready to start conversation');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isCrisisDetected, setIsCrisisDetected] = useState(false);
  const [textInput, setTextInput] = useState('');
  const [showTextMode, setShowTextMode] = useState(false);
  
  // Refs
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  
  // Check API health on mount
  useEffect(() => {
    checkApiHealth();
  }, []);
  
  const checkApiHealth = async () => {
    try {
      const response = await fetch(`${API_BASE}/health`);
      const data = await response.json();
      if (data.status === 'ok' && data.ai_system === 'initialized') {
        setStatus('🇴🇲 Ready for Omani Arabic conversation');
      } else {
        setStatus('⚠️ AI system not fully initialized');
      }
    } catch (error) {
      setStatus('❌ Cannot connect to backend');
    }
  };
  
  // Voice recording functions
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
      setStatus('🎤 Recording... Speak in Arabic');
    } catch (err) {
      setStatus('❌ Microphone access denied. Please allow microphone access.');
    }
  };
  
  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
    setRecording(false);
    setStatus('🎵 Recording complete. Ready to process.');
  };
  
  // Process audio with backend
  const processAudio = async () => {
    if (!audioBlob) return;
    
    setIsProcessing(true);
    setStatus('🔄 Processing audio...');
    setCurrentUserText('');
    setCurrentAiResponse('');
    setTtsAudioURL(null);
    setIsCrisisDetected(false);
    
    try {
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.webm');
      
      const response = await fetch(`${API_BASE}/audio`, {
        method: 'POST',
        body: formData,
      });
      
      const data: ApiResponse = await response.json();
      
      if (data.error) {
        setStatus(`❌ ${data.error}`);
        return;
      }
      
      // Update UI with results
      const userText = data.recognized_text || '';
      const aiResponse = data.ai_response || '';
      
      setCurrentUserText(userText);
      setCurrentAiResponse(aiResponse);
      setIsCrisisDetected(data.is_crisis_detected || false);
      
      // Add to conversation history
      if (userText && aiResponse) {
        const newTurn: ConversationTurn = {
          userText,
          aiResponse,
          timestamp: data.timestamp || Date.now(),
          isCrisis: data.is_crisis_detected || false
        };
        setConversationHistory(prev => [...prev, newTurn]);
      }
      
      // Handle TTS audio
      if (data.tts_audio_base64) {
        const audioBlob = b64toBlob(data.tts_audio_base64, 'audio/wav');
        const audioURL = URL.createObjectURL(audioBlob);
        setTtsAudioURL(audioURL);
        
        // Auto-play TTS response
        setTimeout(() => playTTSAudio(audioURL), 500);
      }
      
      setStatus(data.is_crisis_detected 
        ? '🚨 Crisis detected - Professional help recommended' 
        : '✅ Response generated successfully');
        
    } catch (error) {
      setStatus('❌ Error processing audio. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };
  
  // Process text input
  const processText = async () => {
    if (!textInput.trim()) return;
    
    setIsProcessing(true);
    setStatus('🔄 Processing text...');
    setCurrentUserText('');
    setCurrentAiResponse('');
    setTtsAudioURL(null);
    setIsCrisisDetected(false);
    
    try {
      const formData = new FormData();
      formData.append('text', textInput.trim());
      
      const response = await fetch(`${API_BASE}/text`, {
        method: 'POST',
        body: formData,
      });
      
      const data: ApiResponse = await response.json();
      
      if (data.error) {
        setStatus(`❌ ${data.error}`);
        return;
      }
      
      const userText = data.user_text || textInput;
      const aiResponse = data.ai_response || '';
      
      setCurrentUserText(userText);
      setCurrentAiResponse(aiResponse);
      setIsCrisisDetected(data.is_crisis_detected || false);
      
      // Add to conversation history
      if (userText && aiResponse) {
        const newTurn: ConversationTurn = {
          userText,
          aiResponse,
          timestamp: data.timestamp || Date.now(),
          isCrisis: data.is_crisis_detected || false
        };
        setConversationHistory(prev => [...prev, newTurn]);
      }
      
      // Handle TTS audio
      if (data.tts_audio_base64) {
        const audioBlob = b64toBlob(data.tts_audio_base64, 'audio/wav');
        const audioURL = URL.createObjectURL(audioBlob);
        setTtsAudioURL(audioURL);
      }
      
      setStatus(data.is_crisis_detected 
        ? '🚨 Crisis detected - Professional help recommended' 
        : '✅ Response generated successfully');
      
      setTextInput(''); // Clear input
        
    } catch (error) {
      setStatus('❌ Error processing text. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };
  
  // Play TTS audio
  const playTTSAudio = (audioURL?: string) => {
    const url = audioURL || ttsAudioURL;
    if (!url) return;
    
    if (audioRef.current) {
      audioRef.current.pause();
    }
    
    const audio = new Audio(url);
    audioRef.current = audio;
    
    audio.onplay = () => setIsPlayingTTS(true);
    audio.onended = () => setIsPlayingTTS(false);
    audio.onerror = () => {
      setIsPlayingTTS(false);
      setStatus('❌ Error playing audio response');
    };
    
    audio.play().catch(() => {
      setStatus('❌ Could not play audio. Please try again.');
    });
  };
  
  // Reset session
  const resetSession = async () => {
    try {
      await fetch(`${API_BASE}/session/reset`, { method: 'POST' });
      setConversationHistory([]);
      setCurrentUserText('');
      setCurrentAiResponse('');
      setTtsAudioURL(null);
      setIsCrisisDetected(false);
      setStatus('🔄 Session reset. Ready for new conversation.');
    } catch (error) {
      setStatus('❌ Error resetting session');
    }
  };
  
  // Download transcript
  const downloadTranscript = async () => {
    try {
      const response = await fetch(`${API_BASE}/session/transcript`);
      const data = await response.json();
      if (data.transcript_file) {
        setStatus(`📄 Transcript saved: ${data.transcript_file}`);
      }
    } catch (error) {
      setStatus('❌ Error generating transcript');
    }
  };
  
  return (
    <div className="app">
      <header className="app-header">
        <h1>🇴🇲 Omani Therapist AI</h1>
        <p className="subtitle">Voice-enabled mental health support in Omani Arabic</p>
      </header>
      
      <main className="app-main">
        {/* Status Bar */}
        <div className={`status-bar ${isCrisisDetected ? 'crisis' : ''}`}>
          {status}
        </div>
        
        {/* Crisis Alert */}
        {isCrisisDetected && (
          <div className="crisis-alert">
            <h3>🚨 Crisis Support</h3>
            <p>If you're in immediate danger, please contact emergency services or a crisis helpline.</p>
            <p>Consider reaching out to a mental health professional for support.</p>
          </div>
        )}
        
        {/* Mode Toggle */}
        <div className="mode-toggle">
          <button 
            className={!showTextMode ? 'active' : ''}
            onClick={() => setShowTextMode(false)}
          >
            🎤 Voice Mode
          </button>
          <button 
            className={showTextMode ? 'active' : ''}
            onClick={() => setShowTextMode(true)}
          >
            ⌨️ Text Mode
          </button>
        </div>
        
        {/* Voice Mode */}
        {!showTextMode && (
          <div className="voice-section">
            <div className="recording-controls">
              <button
                className={`record-btn ${recording ? 'recording' : ''}`}
                onClick={recording ? stopRecording : startRecording}
                disabled={isProcessing}
              >
                {recording ? '🛑 Stop Recording' : '🎤 Start Recording'}
              </button>
              
              {audioURL && (
                <div className="audio-preview">
                  <audio controls src={audioURL} />
                </div>
              )}
              
              <button
                className="process-btn"
                onClick={processAudio}
                disabled={!audioBlob || recording || isProcessing}
              >
                {isProcessing ? '🔄 Processing...' : '🚀 Process Audio'}
              </button>
            </div>
          </div>
        )}
        
        {/* Text Mode */}
        {showTextMode && (
          <div className="text-section">
            <div className="text-input-area">
              <textarea
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                placeholder="Type your message in Arabic or English..."
                rows={4}
                disabled={isProcessing}
              />
              <button
                className="process-btn"
                onClick={processText}
                disabled={!textInput.trim() || isProcessing}
              >
                {isProcessing ? '🔄 Processing...' : '📤 Send Message'}
              </button>
            </div>
          </div>
        )}
        
        {/* Current Conversation */}
        {(currentUserText || currentAiResponse) && (
          <div className="current-conversation">
            {currentUserText && (
              <div className="message user-message">
                <strong>You:</strong> {currentUserText}
              </div>
            )}
            
            {currentAiResponse && (
              <div className="message ai-message">
                <strong>Therapist:</strong> {currentAiResponse}
                {ttsAudioURL && (
                  <button
                    className="play-audio-btn"
                    onClick={() => playTTSAudio()}
                    disabled={isPlayingTTS}
                  >
                    {isPlayingTTS ? '🔊 Playing...' : '🔊 Play Response'}
                  </button>
                )}
              </div>
            )}
          </div>
        )}
        
        {/* Session Controls */}
        <div className="session-controls">
          <button onClick={resetSession} className="secondary-btn">
            🔄 Reset Session
          </button>
          <button onClick={downloadTranscript} className="secondary-btn">
            📄 Download Transcript
          </button>
          <button onClick={checkApiHealth} className="secondary-btn">
            🔍 Check Status
          </button>
        </div>
        
        {/* Conversation History (Expandable) */}
        {conversationHistory.length > 0 && (
          <div className="conversation-history">
            <h3>📝 Conversation History</h3>
            <div className="history-list">
              {conversationHistory.slice(-5).map((turn, index) => (
                <div key={index} className={`history-item ${turn.isCrisis ? 'crisis-turn' : ''}`}>
                  <div className="history-user">You: {turn.userText}</div>
                  <div className="history-ai">Therapist: {turn.aiResponse}</div>
                  {turn.isCrisis && <div className="crisis-indicator">🚨 Crisis detected</div>}
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
      
      <footer className="app-footer">
        <p>🔒 Confidential mental health support • Cultural sensitivity built-in</p>
        <p>⚠️ This is an AI assistant, not a replacement for professional therapy</p>
      </footer>
    </div>
  );
};

export default App;
