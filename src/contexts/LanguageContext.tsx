import React, { createContext, useContext, useState, ReactNode } from 'react';

interface LanguageContextType {
  currentLanguage: string;
  setLanguage: (language: string) => void;
  translate: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

// Translations
const translations: Record<string, Record<string, string>> = {
  en: {
    // Navigation
    'nav.dashboard': 'Dashboard',
    'nav.chat': 'AI Assistant',
    'nav.agents': 'Agents',
    'nav.profile': 'Profile',
    'nav.logout': 'Logout',
    
    // Common
    'common.loading': 'Loading...',
    'common.error': 'Error',
    'common.success': 'Success',
    'common.submit': 'Submit',
    'common.cancel': 'Cancel',
    'common.save': 'Save',
    'common.delete': 'Delete',
    'common.edit': 'Edit',
    
    // Home Page
    'home.title': 'Agriculture AI Assistant',
    'home.subtitle': 'Smart farming decisions with AI-powered insights',
    'home.cta.login': 'Login',
    'home.cta.register': 'Get Started',
    
    // Authentication
    'auth.login.title': 'Login to Your Account',
    'auth.register.title': 'Create Your Account',
    'auth.email': 'Email',
    'auth.password': 'Password',
    'auth.fullName': 'Full Name',
    'auth.phone': 'Phone Number',
    'auth.location': 'Location',
    'auth.userType': 'User Type',
    'auth.farmSize': 'Farm Size',
    
    // Chat
    'chat.placeholder': 'Ask me about crops, weather, market prices...',
    'chat.send': 'Send',
    'chat.typing': 'AI is thinking...',
    
    // Dashboard
    'dashboard.welcome': 'Welcome',
    'dashboard.quickActions': 'Quick Actions',
    'dashboard.recentActivity': 'Recent Activity',
    
    // Agents
    'agents.title': 'AI Agents',
    'agents.description': 'Specialized agents for different agricultural needs',
  },
  hi: {
    // Navigation
    'nav.dashboard': 'डैशबोर्ड',
    'nav.chat': 'AI सहायक',
    'nav.agents': 'एजेंट्स',
    'nav.profile': 'प्रोफाइल',
    'nav.logout': 'लॉगआउट',
    
    // Common
    'common.loading': 'लोड हो रहा है...',
    'common.error': 'त्रुटि',
    'common.success': 'सफलता',
    'common.submit': 'जमा करें',
    'common.cancel': 'रद्द करें',
    'common.save': 'सेव करें',
    'common.delete': 'हटाएं',
    'common.edit': 'संपादित करें',
    
    // Home Page
    'home.title': 'कृषि AI सहायक',
    'home.subtitle': 'AI-संचालित अंतर्दृष्टि के साथ स्मार्ट कृषि निर्णय',
    'home.cta.login': 'लॉगिन',
    'home.cta.register': 'शुरू करें',
    
    // Authentication
    'auth.login.title': 'अपने खाते में लॉगिन करें',
    'auth.register.title': 'अपना खाता बनाएं',
    'auth.email': 'ईमेल',
    'auth.password': 'पासवर्ड',
    'auth.fullName': 'पूरा नाम',
    'auth.phone': 'फोन नंबर',
    'auth.location': 'स्थान',
    'auth.userType': 'उपयोगकर्ता प्रकार',
    'auth.farmSize': 'खेत का आकार',
    
    // Chat
    'chat.placeholder': 'फसलों, मौसम, बाजार की कीमतों के बारे में पूछें...',
    'chat.send': 'भेजें',
    'chat.typing': 'AI सोच रहा है...',
    
    // Dashboard
    'dashboard.welcome': 'स्वागत है',
    'dashboard.quickActions': 'त्वरित क्रियाएं',
    'dashboard.recentActivity': 'हाल की गतिविधि',
    
    // Agents
    'agents.title': 'AI एजेंट्स',
    'agents.description': 'विभिन्न कृषि आवश्यकताओं के लिए विशेष एजेंट्स',
  }
};

interface LanguageProviderProps {
  children: ReactNode;
}

export const LanguageProvider: React.FC<LanguageProviderProps> = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');

  const setLanguage = (language: string) => {
    setCurrentLanguage(language);
    localStorage.setItem('language', language);
  };

  const translate = (key: string): string => {
    return translations[currentLanguage]?.[key] || translations.en[key] || key;
  };

  const value: LanguageContextType = {
    currentLanguage,
    setLanguage,
    translate,
  };

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
};