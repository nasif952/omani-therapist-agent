import React, { useState, useEffect } from 'react';
import './App.css';
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';

type AppView = 'landing' | 'dashboard';

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<AppView>('landing');
  const [apiHealth, setApiHealth] = useState<'checking' | 'healthy' | 'unhealthy'>('checking');
  
  // Check API health on mount
  useEffect(() => {
    checkApiHealth();
  }, []);
  
  const checkApiHealth = async () => {
    try {
      const response = await fetch('/api/health');
      const data = await response.json();
      if (data.status === 'ok' && data.ai_system === 'initialized') {
        setApiHealth('healthy');
      } else {
        setApiHealth('unhealthy');
      }
    } catch (error) {
      setApiHealth('unhealthy');
    }
  };
  
  const handleGetStarted = () => {
    if (apiHealth === 'healthy') {
      setCurrentView('dashboard');
    } else {
      // Show error or retry
      checkApiHealth();
    }
  };

  const handleBackToLanding = () => {
    setCurrentView('landing');
  };
  
  // API Health Check Banner
  const renderHealthBanner = () => {
    if (apiHealth === 'checking') {
      return (
        <div className="health-banner checking">
          <div className="banner-content">
            <span className="banner-icon">🔄</span>
            <span>Checking system status...</span>
          </div>
        </div>
      );
      }
      
    if (apiHealth === 'unhealthy') {
      return (
        <div className="health-banner unhealthy">
          <div className="banner-content">
            <span className="banner-icon">⚠️</span>
            <span>System unavailable. Please check backend connection.</span>
            <button className="retry-button" onClick={checkApiHealth}>
              Retry
            </button>
          </div>
        </div>
      );
      }
    
    return null;
  };
  
  return (
    <div className="app">
      {renderHealthBanner()}
      
      {currentView === 'landing' ? (
        <LandingPage onGetStarted={handleGetStarted} />
      ) : (
        <Dashboard onBackToLanding={handleBackToLanding} />
      )}
    </div>
  );
};

export default App;