import React, { useState, useRef } from 'react';
import { Mic, MicOff, Volume2 } from 'lucide-react';

interface VoiceInputProps {
  onTranscript: (text: string) => void;
  onSpeech: (text: string) => void;
  language?: string;
}

const VoiceInput: React.FC<VoiceInputProps> = ({ 
  onTranscript, 
  onSpeech, 
  language = 'en-IN' 
}) => {
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const recognitionRef = useRef<any>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);

  // Initialize speech recognition
  const initializeSpeechRecognition = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = language;
      
      recognitionRef.current.onstart = () => {
        setIsListening(true);
      };
      
      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        onTranscript(transcript);
        setIsListening(false);
      };
      
      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };
      
      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  };

  // Start voice recognition
  const startListening = () => {
    if (!recognitionRef.current) {
      initializeSpeechRecognition();
    }
    
    if (recognitionRef.current && !isListening) {
      try {
        recognitionRef.current.start();
      } catch (error) {
        console.error('Error starting speech recognition:', error);
      }
    }
  };

  // Stop voice recognition
  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
    }
  };

  // Text-to-speech
  const speakText = (text: string) => {
    if ('speechSynthesis' in window) {
      // Cancel any ongoing speech
      window.speechSynthesis.cancel();
      
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = language;
      utterance.rate = 0.9;
      utterance.pitch = 1;
      
      utterance.onstart = () => {
        setIsSpeaking(true);
      };
      
      utterance.onend = () => {
        setIsSpeaking(false);
      };
      
      utterance.onerror = () => {
        setIsSpeaking(false);
      };
      
      window.speechSynthesis.speak(utterance);
      onSpeech(text);
    }
  };

  // Stop speech
  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  return (
    <div className="flex items-center space-x-2">
      {/* Voice Input Button */}
      <button
        onClick={isListening ? stopListening : startListening}
        className={`p-2 rounded-full transition-colors ${
          isListening
            ? 'bg-red-100 text-red-600 hover:bg-red-200'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        }`}
        title={isListening ? 'Stop listening' : 'Start voice input'}
      >
        {isListening ? (
          <MicOff className="h-4 w-4" />
        ) : (
          <Mic className="h-4 w-4" />
        )}
      </button>

      {/* Text-to-Speech Button */}
      <button
        onClick={isSpeaking ? stopSpeaking : () => speakText('Hello, I am your AI agriculture assistant')}
        className={`p-2 rounded-full transition-colors ${
          isSpeaking
            ? 'bg-blue-100 text-blue-600 hover:bg-blue-200'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        }`}
        title={isSpeaking ? 'Stop speaking' : 'Test voice output'}
      >
        <Volume2 className="h-4 w-4" />
      </button>

      {/* Status Indicator */}
      {isListening && (
        <div className="flex items-center space-x-2 text-red-600 text-sm">
          <div className="animate-pulse flex items-center space-x-1">
            <div className="h-2 w-2 bg-red-600 rounded-full"></div>
            <span>Listening...</span>
          </div>
        </div>
      )}

      {isSpeaking && (
        <div className="flex items-center space-x-2 text-blue-600 text-sm">
          <div className="animate-pulse flex items-center space-x-1">
            <div className="h-2 w-2 bg-blue-600 rounded-full"></div>
            <span>Speaking...</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default VoiceInput;