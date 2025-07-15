import React, { useState } from 'react';
import MicStreamTranscriber from '../MicStreamTranscriber';

interface RealTimeModeProps {
  onCrisisDetected: (detected: boolean) => void;
}

const RealTimeMode: React.FC<RealTimeModeProps> = ({ onCrisisDetected }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('Ready to connect');

  return (
    <div className="realtime-mode">
      {/* Status Bar */}
      <div className="realtime-status">
        <div className="status-content">
          <div className="status-icon">
            {isConnected ? '🟢' : '⚡'}
          </div>
          <span className="status-text">{connectionStatus}</span>
        </div>
      </div>

      {/* Real-time Info */}
      <div className="realtime-info">
        <div className="info-card">
          <div className="info-header">
            <h3>Real-time Voice Processing</h3>
            <p>Advanced voice activity detection and live transcription</p>
          </div>
          
          <div className="info-features">
            <div className="feature-grid">
              <div className="feature-item">
                <div className="feature-icon">🎯</div>
                <div className="feature-content">
                  <h4>Voice Activity Detection</h4>
                  <p>Intelligent detection of speech vs silence</p>
                </div>
              </div>
              <div className="feature-item">
                <div className="feature-icon">📝</div>
                <div className="feature-content">
                  <h4>Live Transcription</h4>
                  <p>Real-time speech-to-text conversion</p>
                </div>
              </div>
              <div className="feature-item">
                <div className="feature-icon">🧠</div>
                <div className="feature-content">
                  <h4>AI Processing</h4>
                  <p>Immediate AI response generation</p>
                </div>
              </div>
              <div className="feature-item">
                <div className="feature-icon">🔊</div>
                <div className="feature-content">
                  <h4>Audio Playback</h4>
                  <p>Text-to-speech response delivery</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Connection Instructions */}
      <div className="connection-guide">
        <div className="guide-card">
          <div className="guide-header">
            <h3>How to Use Real-time Mode</h3>
          </div>
          
          <div className="guide-steps">
            <div className="step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h4>Connect Microphone</h4>
                <p>Click "Start Recording" to begin real-time processing</p>
              </div>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h4>Speak Naturally</h4>
                <p>Talk in Arabic or English - the system will detect when you're speaking</p>
              </div>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h4>Get Instant Responses</h4>
                <p>AI will process your speech and respond immediately</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Real-time Transcriber Component */}
      <div className="transcriber-section">
        <div className="transcriber-card">
          <div className="transcriber-header">
            <h3>Live Transcription & Processing</h3>
            <p>WebSocket-based real-time communication</p>
          </div>
          
          <div className="transcriber-content">
            <MicStreamTranscriber />
          </div>
        </div>
      </div>

      {/* Technical Info */}
      <div className="technical-info">
        <div className="tech-card">
          <div className="tech-header">
            <h3>Technical Specifications</h3>
          </div>
          
          <div className="tech-specs">
            <div className="spec-group">
              <h4>Audio Processing</h4>
              <ul>
                <li>Sample Rate: 16kHz</li>
                <li>Channels: Mono (1 channel)</li>
                <li>Format: PCM 16-bit</li>
                <li>Buffer Size: 4096 samples</li>
              </ul>
            </div>
            
            <div className="spec-group">
              <h4>Connection</h4>
              <ul>
                <li>Protocol: WebSocket</li>
                <li>Endpoint: ws://localhost:8000/ws/audio</li>
                <li>Real-time: Low latency streaming</li>
                <li>Reconnection: Automatic retry</li>
              </ul>
            </div>
            
            <div className="spec-group">
              <h4>Features</h4>
              <ul>
                <li>Voice Activity Detection (VAD)</li>
                <li>Noise Suppression</li>
                <li>Echo Cancellation</li>
                <li>Crisis Detection</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="performance-metrics">
        <div className="metrics-card">
          <div className="metrics-header">
            <h3>Performance Metrics</h3>
          </div>
          
          <div className="metrics-grid">
            <div className="metric">
              <div className="metric-value">~100ms</div>
              <div className="metric-label">Audio Latency</div>
            </div>
            <div className="metric">
              <div className="metric-value">~200ms</div>
              <div className="metric-label">Transcription Delay</div>
            </div>
            <div className="metric">
              <div className="metric-value">~1-2s</div>
              <div className="metric-label">AI Response Time</div>
            </div>
            <div className="metric">
              <div className="metric-value">16kHz</div>
              <div className="metric-label">Audio Quality</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RealTimeMode; 