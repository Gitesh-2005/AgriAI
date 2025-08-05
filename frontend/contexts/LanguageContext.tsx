import React, { createContext, useContext, useState, ReactNode } from 'react';

interface LanguageContextType {
  language: string;
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

interface LanguageProviderProps {
  children: ReactNode;
}

export const LanguageProvider: React.FC<LanguageProviderProps> = ({ children }) => {
  const [language, setLanguage] = useState('en');

  const translate = (key: string): string => {
    const translations: Record<string, Record<string, string>> = {
      en: {
        welcome: 'Welcome',
        login: 'Login',
        register: 'Register',
      },
      es: {
        welcome: 'Bienvenido',
        login: 'Iniciar sesión',
        register: 'Registrarse',
      },
    };

    return translations[language]?.[key] || key;
  };

  const value = {
    language,
    setLanguage,
    translate,
  };

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
};