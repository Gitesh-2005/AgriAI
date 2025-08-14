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
  const [audioURL, setAudioURL] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);
  const [transcript, setTranscript] = useState<string | null>(null);
  const [interim, setInterim] = useState<string | null>(null);
  const recognitionRef = useRef<any>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);

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

  const startRecording = async () => {
    setTranscript(null);
    setInterim(null);
    setAudioURL(null);
    setIsListening(true);
    setProcessing(false);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorderRef.current = mediaRecorder;
    audioChunks.current = [];

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.current.push(event.data);
      }
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
      setAudioURL(URL.createObjectURL(audioBlob));
      setInterim('Processing...');
      setProcessing(true);
      // Send to backend
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.webm');
      formData.append('language', language); // Pass language to backend
      try {
        const res = await fetch('http://localhost:8000/api/v1/stt/transcribe/', {
          method: 'POST',
          body: formData,
        });
        const data = await res.json();
        setTranscript(data.translation); // Use translation
        setInterim(null);
      } catch (err) {
        setTranscript('Transcription failed.');
        setInterim(null);
      }
      setProcessing(false);
    };

    mediaRecorder.start();
  };

  const stopRecording = () => {
    setIsListening(false);
    mediaRecorderRef.current?.stop();
  };

  return (
    <div className="flex flex-col items-center space-y-4">
      {/* Voice Input Button */}
      <button
        onClick={isListening ? stopRecording : startRecording}
        className={`px-6 py-3 rounded-full font-bold text-white ${
          isListening
            ? 'bg-red-500'
            : 'bg-green-600'
        } transition-colors`}
        title={isListening ? 'Stop listening' : 'Start voice input'}
      >
        {isListening ? 'Stop Recording' : 'Start Voice Input'}
      </button>

      {/* Audio Playback */}
      {audioURL && (
        <audio controls src={audioURL} className="mt-2" />
      )}

      {/* Interim Transcript */}
      {interim && (
        <div className="text-blue-600 font-medium">You said: ... {interim}</div>
      )}

      {/* Processing Indicator */}
      {processing && (
        <div className="text-gray-500">Processing...</div>
      )}

      {/* Final Transcript */}
      {transcript && (
        <div className="text-green-700 font-semibold">Transcription: {transcript}</div>
      )}

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