import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, MicOff, Bot, User, Loader2 } from 'lucide-react';
import { useMutation, useQuery } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { chatAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  agent?: string;
  confidence?: number;
  metadata?: any;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const [isListening, setIsListening] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  const { user } = useAuth();
  const { translate } = useLanguage();

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Send message mutation
  const sendMessageMutation = useMutation({
    mutationFn: (messageData: any) => chatAPI.sendMessage(messageData),
    onSuccess: (response) => {
      const assistantMessage: Message = {
        id: `assistant_${Date.now()}`,
        type: 'assistant',
        content: response.response,
        timestamp: new Date(),
        agent: response.agent_used,
        confidence: response.confidence,
        metadata: response.metadata,
      };
      setMessages(prev => [...prev, assistantMessage]);
      
      if (response.confidence < 0.5) {
        toast('The AI response has low confidence. Consider rephrasing your question.', {
          icon: '⚠️',
        });
      }
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.detail || 'Failed to send message');
      
      // Add error message
      const errorMessage: Message = {
        id: `error_${Date.now()}`,
        type: 'assistant',
        content: 'Sorry, I encountered an error while processing your message. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    },
  });

  const handleSendMessage = async () => {
    if (!inputValue.trim() || sendMessageMutation.isPending) return;

    const userMessage: Message = {
      id: `user_${Date.now()}`,
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const messageContent = inputValue.trim();
    setInputValue('');

    // Send to API
    sendMessageMutation.mutate({
      message: messageContent,
      session_id: sessionId,
      language: user?.language_preference || 'en',
      context: {
        location: user?.location,
        user_type: user?.user_type,
        farm_size: user?.farm_size,
      },
    });
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Voice recognition (basic implementation)
  const toggleVoiceRecording = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
      const recognition = new SpeechRecognition();
      
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = user?.language_preference === 'hi' ? 'hi-IN' : 'en-IN';
      
      if (!isListening) {
        setIsListening(true);
        recognition.start();
        
        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setInputValue(transcript);
          setIsListening(false);
        };
        
        recognition.onerror = () => {
          setIsListening(false);
          toast.error('Voice recognition failed. Please try again.');
        };
        
        recognition.onend = () => {
          setIsListening(false);
        };
      } else {
        recognition.stop();
        setIsListening(false);
      }
    } else {
      toast.error('Voice recognition is not supported in your browser.');
    }
  };

  // Sample questions for new users
  const sampleQuestions = [
    "What crops should I grow this season?",
    "Check weather forecast for farming",
    "What are today's market prices for rice?",
    "How to prepare soil for wheat planting?",
    "Best irrigation schedule for cotton crop",
    "Government subsidies for farmers",
    "Pest control for tomato plants",
    "Soil testing and fertilizer recommendations",
    "Crop insurance and loan information",
    "Agricultural policies and regulations"
  ];

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col bg-white rounded-2xl shadow-lg overflow-hidden">
      {/* Chat Header */}
      <div className="bg-gradient-to-r from-green-500 to-blue-600 p-4 text-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-white/20 rounded-full">
              <Bot className="h-6 w-6" />
            </div>
            <div>
              <h2 className="font-semibold">AI Agriculture Assistant</h2>
              <p className="text-sm text-green-100">
                Ask me anything about farming, weather, markets, and more
              </p>
            </div>
          </div>
          {sendMessageMutation.isPending && (
            <div className="flex items-center space-x-2 text-green-100">
              <Loader2 className="h-4 w-4 animate-spin" />
              <span className="text-sm">{translate('chat.typing')}</span>
            </div>
          )}
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-6">
            <div className="p-4 bg-gradient-to-r from-green-100 to-blue-100 rounded-full">
              <Bot className="h-12 w-12 text-green-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Welcome to your AI farming assistant!
              </h3>
              <p className="text-gray-600 mb-6 max-w-md">
                I can help you with crop advisory, weather forecasts, market prices, and much more. Try asking one of these questions:
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl">
              {sampleQuestions.map((question, index) => (
                <motion.button
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  onClick={() => setInputValue(question)}
                  className="p-3 text-left bg-gray-50 hover:bg-gray-100 rounded-lg border border-gray-200 hover:border-green-300 transition-all duration-200 text-sm"
                >
                  {question}
                </motion.button>
              ))}
            </div>
          </div>
        ) : (
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md xl:max-w-lg ${
                    message.type === 'user'
                      ? 'bg-gradient-to-r from-green-500 to-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  } rounded-2xl px-4 py-3 shadow-sm`}
                >
                  <div className="flex items-start space-x-2">
                    {message.type === 'assistant' && (
                      <Bot className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                    )}
                    {message.type === 'user' && (
                      <User className="h-5 w-5 text-white mt-0.5 flex-shrink-0" />
                    )}
                    <div className="flex-1">
                      <div className="whitespace-pre-wrap text-sm leading-relaxed">
                        {message.content}
                      </div>
                      {message.type === 'assistant' && message.agent && (
                        <div className="mt-2 pt-2 border-t border-gray-200 flex items-center justify-between text-xs text-gray-500">
                          <span>Agent: {message.agent}</span>
                          {message.confidence && (
                            <span>
                              Confidence: {Math.round(message.confidence * 100)}%
                            </span>
                          )}
                        </div>
                      )}
                      <div className="text-xs opacity-75 mt-1">
                        {message.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4 bg-gray-50">
        <div className="flex items-center space-x-3">
          <div className="flex-1 relative">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={translate('chat.placeholder')}
              disabled={sendMessageMutation.isPending}
              className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <button
              onClick={toggleVoiceRecording}
              className={`absolute right-3 top-1/2 transform -translate-y-1/2 p-1.5 rounded-full transition-colors ${
                isListening
                  ? 'bg-red-100 text-red-600 hover:bg-red-200'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {isListening ? (
                <MicOff className="h-4 w-4" />
              ) : (
                <Mic className="h-4 w-4" />
              )}
            </button>
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || sendMessageMutation.isPending}
            className="p-3 bg-gradient-to-r from-green-500 to-blue-600 text-white rounded-full hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 disabled:transform-none"
          >
            {sendMessageMutation.isPending ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </button>
        </div>
        
        {isListening && (
          <div className="mt-2 flex items-center justify-center text-sm text-red-600">
            <div className="animate-pulse flex items-center space-x-2">
              <div className="h-2 w-2 bg-red-600 rounded-full"></div>
              <span>Listening... Speak now</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Chat;