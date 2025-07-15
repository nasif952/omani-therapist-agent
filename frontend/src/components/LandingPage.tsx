import React from 'react';

interface LandingPageProps {
  onGetStarted: () => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onGetStarted }) => {
  return (
    <div className="landing-page">
      {/* Navigation */}
      <nav className="landing-nav">
        <div className="nav-container">
          <div className="nav-logo">
            <span className="logo-icon">🇴🇲</span>
            <span className="logo-text">Omani Companion</span>
          </div>
          <div className="nav-links">
            <a href="#features">Features</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
            <button className="nav-cta" onClick={onGetStarted}>
              Get Started
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-container">
          <div className="hero-content">
            <div className="hero-badge">
              <span className="badge-icon">🛡️</span>
              <span>HIPAA Compliant • Culturally Sensitive</span>
            </div>
            
            <h1 className="hero-title">
              Professional Mental Health Support
              <span className="title-highlight"> for Oman</span>
            </h1>
            
            <p className="hero-description">
              Advanced AI-powered mental health assistance designed specifically for Omani culture. 
              Speak naturally in Arabic or English with our culturally-aware therapeutic companion.
            </p>
            
            <div className="hero-features">
              <div className="feature-item">
                <span className="feature-icon">🎤</span>
                <span>Voice & Text Support</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">🔒</span>
                <span>End-to-End Encrypted</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">🇴🇲</span>
                <span>Omani Arabic Fluent</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">🚨</span>
                <span>Crisis Detection</span>
              </div>
            </div>
            
            <div className="hero-actions">
              <button className="primary-cta" onClick={onGetStarted}>
                <span className="cta-icon">🚀</span>
                Start Your Session
              </button>
              <button className="secondary-cta">
                <span className="cta-icon">📹</span>
                Watch Demo
              </button>
            </div>
            
            <div className="trust-indicators">
              <div className="trust-item">
                <span className="trust-number">24/7</span>
                <span className="trust-label">Available</span>
              </div>
              <div className="trust-item">
                <span className="trust-number">100%</span>
                <span className="trust-label">Confidential</span>
              </div>
              <div className="trust-item">
                <span className="trust-number">5★</span>
                <span className="trust-label">Rated</span>
              </div>
            </div>
          </div>
          
          <div className="hero-visual">
            <div className="visual-container">
              <div className="visual-card main-card">
                <div className="card-header">
                  <div className="card-avatar">🇴🇲</div>
                  <div className="card-info">
                    <div className="card-name">Omani Companion</div>
                    <div className="card-status">
                      <span className="status-dot"></span>
                      Online & Ready
                    </div>
                  </div>
                </div>
                <div className="card-content">
                  <div className="message ai-message">
                    <p>مرحباً! كيف يمكنني مساعدتك اليوم؟</p>
                    <p className="message-translation">Hello! How can I help you today?</p>
                  </div>
                  <div className="message user-message">
                    <p>أحتاج للحديث مع أحد</p>
                  </div>
                </div>
                <div className="card-footer">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
              
              <div className="visual-card feature-card">
                <div className="feature-icon-large">🎤</div>
                <div className="feature-title">Voice Recognition</div>
                <div className="feature-description">Natural Arabic speech processing</div>
              </div>
              
              <div className="visual-card security-card">
                <div className="security-icon">🔒</div>
                <div className="security-title">Secure & Private</div>
                <div className="security-bars">
                  <div className="bar"></div>
                  <div className="bar"></div>
                  <div className="bar"></div>
                  <div className="bar"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section">
        <div className="features-container">
          <div className="section-header">
            <h2 className="section-title">Comprehensive Mental Health Support</h2>
            <p className="section-description">
              Advanced AI technology meets Omani cultural sensitivity to provide 
              professional-grade mental health assistance.
            </p>
          </div>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-header">
                <div className="feature-icon">🎤</div>
                <h3>Voice Interaction</h3>
              </div>
              <p>Speak naturally in Omani Arabic or English. Our advanced speech recognition understands dialects and emotional context.</p>
              <ul className="feature-list">
                <li>Natural language processing</li>
                <li>Omani dialect recognition</li>
                <li>Emotional tone analysis</li>
              </ul>
            </div>
            
            <div className="feature-card">
              <div className="feature-header">
                <div className="feature-icon">💬</div>
                <h3>Text Conversations</h3>
              </div>
              <p>Type your thoughts in Arabic or English. Perfect for those who prefer written communication or need discretion.</p>
              <ul className="feature-list">
                <li>Bilingual text support</li>
                <li>Real-time responses</li>
                <li>Private messaging</li>
              </ul>
            </div>
            
            <div className="feature-card">
              <div className="feature-header">
                <div className="feature-icon">🚨</div>
                <h3>Crisis Detection</h3>
              </div>
              <p>Advanced AI monitors conversations for signs of crisis and provides immediate support resources and professional contacts.</p>
              <ul className="feature-list">
                <li>24/7 crisis monitoring</li>
                <li>Immediate emergency contacts</li>
                <li>Professional referrals</li>
              </ul>
            </div>
            
            <div className="feature-card">
              <div className="feature-header">
                <div className="feature-icon">🕌</div>
                <h3>Cultural Sensitivity</h3>
              </div>
              <p>Built with deep understanding of Omani culture, Islamic values, and traditional approaches to mental wellness.</p>
              <ul className="feature-list">
                <li>Islamic counseling principles</li>
                <li>Family-centered approach</li>
                <li>Cultural respect & privacy</li>
              </ul>
            </div>
            
            <div className="feature-card">
              <div className="feature-header">
                <div className="feature-icon">🔒</div>
                <h3>Privacy & Security</h3>
              </div>
              <p>Enterprise-grade security with end-to-end encryption ensures your conversations remain completely confidential.</p>
              <ul className="feature-list">
                <li>End-to-end encryption</li>
                <li>HIPAA compliance</li>
                <li>Local data processing</li>
              </ul>
            </div>
            
            <div className="feature-card">
              <div className="feature-header">
                <div className="feature-icon">⚡</div>
                <h3>Real-time Processing</h3>
              </div>
              <p>Advanced voice activity detection and real-time transcription for seamless, natural conversations.</p>
              <ul className="feature-list">
                <li>Live transcription</li>
                <li>Voice activity detection</li>
                <li>Instant AI responses</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Emergency Resources */}
      <section className="emergency-section">
        <div className="emergency-container">
          <div className="emergency-content">
            <h2 className="emergency-title">
              <span className="emergency-icon">🚨</span>
              Emergency Mental Health Resources
            </h2>
            <p className="emergency-description">
              If you're experiencing a mental health crisis, professional help is available 24/7.
            </p>
            <div className="emergency-contacts">
              <div className="contact-card">
                <div className="contact-icon">🚑</div>
                <div className="contact-info">
                  <div className="contact-title">Emergency Services</div>
                  <div className="contact-number">999</div>
                </div>
              </div>
              <div className="contact-card">
                <div className="contact-icon">🏥</div>
                <div className="contact-info">
                  <div className="contact-title">Mental Health Support</div>
                  <div className="contact-number">+968 24601999</div>
                </div>
              </div>
              <div className="contact-card">
                <div className="contact-icon">📞</div>
                <div className="contact-info">
                  <div className="contact-title">Crisis Helpline</div>
                  <div className="contact-number">+968 80077000</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-container">
          <div className="cta-content">
            <h2 className="cta-title">Ready to Start Your Mental Health Journey?</h2>
            <p className="cta-description">
              Join thousands of Omanis who trust our AI companion for confidential, 
              culturally-sensitive mental health support.
            </p>
            <button className="cta-button" onClick={onGetStarted}>
              <span className="cta-icon">🚀</span>
              Begin Your Session Now
            </button>
            <p className="cta-note">
              🔒 Completely confidential • 🇴🇲 Culturally respectful • ⚡ Available 24/7
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage; 