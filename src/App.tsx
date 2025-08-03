import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './contexts/AuthContext';
import { LanguageProvider } from './contexts/LanguageContext';

// Components
import Layout from './components/Layout';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Agents from './pages/Agents';
import Profile from './pages/Profile';
import Analytics from './pages/Analytics';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <LanguageProvider>
          <Router>
            <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
                <Route path="/chat" element={<Layout><Chat /></Layout>} />
                <Route path="/agents" element={<Layout><Agents /></Layout>} />
                <Route path="/profile" element={<Layout><Profile /></Layout>} />
                <Route path="/analytics" element={<Layout><Analytics /></Layout>} />
              </Routes>
              <Toaster 
                position="top-right"
                toastOptions={{
                  duration: 4000,
                  style: {
                    background: '#363636',
                    color: '#fff',
                  },
                }}
              />
            </div>
          </Router>
        </LanguageProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;