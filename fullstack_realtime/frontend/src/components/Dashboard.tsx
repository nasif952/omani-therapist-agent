import React, { useState } from 'react';
import VoiceMode from './VoiceMode';
import TextMode from './TextMode';
import RealTimeMode from './RealTimeMode';

interface DashboardProps {
  onBackToLanding: () => void;
}

type ActiveMode = 'voice' | 'text' | 'realtime';

const Dashboard: React.FC<DashboardProps> = ({ onBackToLanding }) => {
  const [activeMode, setActiveMode] = useState<ActiveMode>('voice');
  const [isCrisisDetected, setIsCrisisDetected] = useState(false);

  const modes = [
    {
      id: 'voice' as ActiveMode,
      title: 'Voice Mode',
      description: 'Speak naturally in Arabic or English',
      icon: '🎤',
      color: 'blue'
    },
    {
      id: 'text' as ActiveMode,
      title: 'Text Mode',
      description: 'Type your thoughts and feelings',
      icon: '💬',
      color: 'green'
    },
    {
      id: 'realtime' as ActiveMode,
      title: 'Real-time Processing',
      description: 'Live transcription and analysis',
      icon: '⚡',
      color: 'purple'
    }
  ];

  const renderActiveMode = () => {
    switch (activeMode) {
      case 'voice':
        return <VoiceMode onCrisisDetected={setIsCrisisDetected} />;
      case 'text':
        return <TextMode onCrisisDetected={setIsCrisisDetected} />;
      case 'realtime':
        return <RealTimeMode onCrisisDetected={setIsCrisisDetected} />;
      default:
        return <VoiceMode onCrisisDetected={setIsCrisisDetected} />;
    }
  };

  return (
    <div className="dashboard">
      {/* Dashboard Header */}
      <header className="dashboard-header">
        <div className="header-container">
          <div className="header-left">
            <button className="back-button" onClick={onBackToLanding}>
              <span className="back-icon">←</span>
              <span>Back to Home</span>
            </button>
            <div className="header-logo">
              <span className="logo-icon">🇴🇲</span>
              <div className="logo-info">
                <span className="logo-title">Omani Companion</span>
                <span className="logo-subtitle">Professional Mental Health Support</span>
              </div>
            </div>
          </div>
          
          <div className="header-right">
            <div className="status-indicator">
              <div className="status-dot"></div>
              <span>Secure Session</span>
            </div>
            <div className="session-info">
              <span className="session-time">Session Active</span>
              <span className="session-id">ID: {Math.random().toString(36).substr(2, 9).toUpperCase()}</span>
            </div>
          </div>
        </div>
      </header>

      {/* Crisis Alert */}
      {isCrisisDetected && (
        <div className="crisis-banner">
          <div className="crisis-content">
            <div className="crisis-icon">🚨</div>
            <div className="crisis-text">
              <h3>Crisis Support Available</h3>
              <p>Professional help is available 24/7. Emergency: 999 | Mental Health: +968 24601999</p>
            </div>
            <button className="crisis-action">Get Help Now</button>
          </div>
        </div>
      )}

      {/* Mode Navigation */}
      <nav className="mode-navigation">
        <div className="nav-container">
          <div className="nav-title">
            <h2>Choose Your Interaction Mode</h2>
            <p>Select how you'd like to communicate with your AI companion</p>
          </div>
          
          <div className="mode-tabs">
            {modes.map((mode) => (
              <button
                key={mode.id}
                className={`mode-tab ${activeMode === mode.id ? 'active' : ''} ${mode.color}`}
                onClick={() => setActiveMode(mode.id)}
              >
                <div className="tab-icon">{mode.icon}</div>
                <div className="tab-content">
                  <div className="tab-title">{mode.title}</div>
                  <div className="tab-description">{mode.description}</div>
                </div>
                <div className="tab-indicator"></div>
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="dashboard-main">
        <div className="main-container">
          {/* Mode Header */}
          <div className="mode-header">
            <div className="mode-info">
              <div className="mode-icon-large">
                {modes.find(m => m.id === activeMode)?.icon}
              </div>
              <div className="mode-details">
                <h1 className="mode-title">
                  {modes.find(m => m.id === activeMode)?.title}
                </h1>
                <p className="mode-description">
                  {modes.find(m => m.id === activeMode)?.description}
                </p>
              </div>
            </div>
            
            <div className="mode-actions">
              <button className="action-button secondary">
                <span className="action-icon">📋</span>
                Session History
              </button>
              <button className="action-button secondary">
                <span className="action-icon">⚙️</span>
                Settings
              </button>
              <button className="action-button danger">
                <span className="action-icon">🔄</span>
                New Session
              </button>
            </div>
          </div>

          {/* Active Mode Component */}
          <div className="mode-content">
            {renderActiveMode()}
          </div>
        </div>
      </main>

      {/* Dashboard Footer */}
      <footer className="dashboard-footer">
        <div className="footer-container">
          <div className="footer-left">
            <div className="security-badges">
              <div className="badge">
                <span className="badge-icon">🔒</span>
                <span>End-to-End Encrypted</span>
              </div>
              <div className="badge">
                <span className="badge-icon">🛡️</span>
                <span>HIPAA Compliant</span>
              </div>
              <div className="badge">
                <span className="badge-icon">🇴🇲</span>
                <span>Culturally Sensitive</span>
              </div>
            </div>
          </div>
          
          <div className="footer-right">
            <div className="emergency-quick-access">
              <span className="emergency-label">Emergency:</span>
              <a href="tel:999" className="emergency-link">999</a>
              <span className="separator">|</span>
              <a href="tel:+96824601999" className="emergency-link">+968 24601999</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard; 