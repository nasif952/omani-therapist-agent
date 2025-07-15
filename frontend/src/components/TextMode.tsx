import React, { useState, useRef, useEffect } from 'react';

interface TextModeProps {
  onCrisisDetected: (detected: boolean) => void;
}

interface ConversationTurn {
  userText: string;
  aiResponse: string;
  timestamp: number;
  isCrisis: boolean;
}

const API_BASE = '/api';

const TextMode: React.FC<TextModeProps> = ({ onCrisisDetected }) => {
  // Text input state
  const [textInput, setTextInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [status, setStatus] = useState('Ready to chat');
  
  // Conversation state
  const [currentUserText, setCurrentUserText] = useState('');
  const [currentAiResponse, setCurrentAiResponse] = useState('');
  const [conversationHistory, setConversationHistory] = useState<ConversationTurn[]>([]);
  const [ttsAudioURL, setTtsAudioURL] = useState<string | null>(null);
  const [isPlayingTTS, setIsPlayingTTS] = useState(false);
  
  // Refs
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversationHistory, currentAiResponse]);

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

  const processText = async () => {
    if (!textInput.trim()) return;

    setIsProcessing(true);
    setStatus('🔄 Processing your message...');
    setCurrentUserText('');
    setCurrentAiResponse('');
    setTtsAudioURL(null);

    const messageToSend = textInput.trim();
    setTextInput(''); // Clear input immediately for better UX

    try {
      const formData = new FormData();
      formData.append('text', messageToSend);

      const response = await fetch(`${API_BASE}/text`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        setStatus(`❌ ${data.error}`);
        setTextInput(messageToSend); // Restore text on error
        return;
      }

      const userText = data.user_text || messageToSend;
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
        : '✅ Message processed successfully');
        
    } catch (error) {
      setStatus('❌ Error processing message. Please try again.');
      setTextInput(messageToSend); // Restore text on error
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      processText();
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
    <div className="text-mode">
      {/* Status Bar */}
      <div className="text-status">
        <div className="status-content">
          <div className="status-icon">
            {isProcessing ? '🔄' : '💬'}
          </div>
          <span className="status-text">{status}</span>
        </div>
      </div>

      {/* Chat Interface */}
      <div className="chat-interface">
        <div className="chat-container">
          {/* Chat Messages */}
          <div className="chat-messages">
            {/* Welcome Message */}
            {conversationHistory.length === 0 && !currentUserText && (
              <div className="welcome-message">
                <div className="welcome-avatar">🇴🇲</div>
                <div className="welcome-content">
                  <h3>مرحباً بك في مرافق عُماني</h3>
                  <p>Welcome to Omani Companion</p>
                  <p className="welcome-description">
                    I'm here to provide professional mental health support in a culturally sensitive way. 
                    You can type in Arabic or English, and I'll respond appropriately.
                  </p>
                  <div className="welcome-features">
                    <div className="feature">🔒 Completely confidential</div>
                    <div className="feature">🇴🇲 Culturally aware</div>
                    <div className="feature">🚨 Crisis detection</div>
                  </div>
                </div>
              </div>
            )}

            {/* Conversation History */}
            {conversationHistory.map((turn, index) => (
              <div key={index} className="message-group">
                <div className="message user-message">
                  <div className="message-avatar">👤</div>
                  <div className="message-content">
                    <div className="message-header">
                      <span className="message-sender">You</span>
                      <span className="message-time">
                        {new Date(turn.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                    <div className="message-text">{turn.userText}</div>
                  </div>
                </div>
                
                <div className={`message ai-message ${turn.isCrisis ? 'crisis-message' : ''}`}>
                  <div className="message-avatar">🇴🇲</div>
                  <div className="message-content">
                    <div className="message-header">
                      <span className="message-sender">Omani Companion</span>
                      <span className="message-time">
                        {new Date(turn.timestamp).toLocaleTimeString()}
                      </span>
                      {turn.isCrisis && <span className="crisis-badge">🚨 Crisis</span>}
                    </div>
                    <div className="message-text">{turn.aiResponse}</div>
                  </div>
                </div>
              </div>
            ))}

            {/* Current Conversation */}
            {currentUserText && (
              <div className="message-group current">
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
                
                {currentAiResponse ? (
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
                ) : isProcessing && (
                  <div className="message ai-message typing">
                    <div className="message-avatar">🇴🇲</div>
                    <div className="message-content">
                      <div className="message-header">
                        <span className="message-sender">Omani Companion</span>
                        <span className="message-time">typing...</span>
                      </div>
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="chat-input-area">
            <div className="input-container">
              <div className="input-wrapper">
                <textarea
                  ref={textareaRef}
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="اكتب رسالتك هنا... أو Type your message here..."
                  disabled={isProcessing}
                  rows={1}
                  className="message-input"
                />
                <div className="input-actions">
                  <div className="input-hints">
                    <span className="hint">Press Enter to send • Shift+Enter for new line</span>
                  </div>
                  <button 
                    className="send-button"
                    onClick={processText}
                    disabled={isProcessing || !textInput.trim()}
                  >
                    <span className="send-icon">
                      {isProcessing ? '🔄' : '📤'}
                    </span>
                    {isProcessing ? 'Sending...' : 'Send'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <div className="actions-header">
          <h4>Quick Actions</h4>
        </div>
        <div className="actions-grid">
          <button 
            className="quick-action"
            onClick={() => setTextInput('أحتاج للحديث مع أحد')}
            disabled={isProcessing}
          >
            <span className="action-icon">💬</span>
            <span>I need to talk</span>
          </button>
          <button 
            className="quick-action"
            onClick={() => setTextInput('أشعر بالقلق')}
            disabled={isProcessing}
          >
            <span className="action-icon">😰</span>
            <span>I feel anxious</span>
          </button>
          <button 
            className="quick-action"
            onClick={() => setTextInput('أحتاج نصيحة')}
            disabled={isProcessing}
          >
            <span className="action-icon">💡</span>
            <span>I need advice</span>
          </button>
          <button 
            className="quick-action"
            onClick={() => setTextInput('كيف يمكنني التعامل مع الضغط؟')}
            disabled={isProcessing}
          >
            <span className="action-icon">🧘</span>
            <span>Stress management</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default TextMode; 