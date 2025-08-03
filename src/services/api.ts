import axios, { AxiosResponse } from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (credentials: { email: string; password: string }) => {
    const response: AxiosResponse = await api.post('/auth/login', credentials);
    return response.data;
  },
  
  register: async (userData: any) => {
    const response: AxiosResponse = await api.post('/auth/register', userData);
    return response.data;
  },
  
  getCurrentUser: async (token: string) => {
    const response: AxiosResponse = await api.get('/auth/me', {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  },
};

// Chat API
export const chatAPI = {
  sendMessage: async (data: {
    message: string;
    session_id?: string;
    context?: any;
    language?: string;
  }) => {
    const response: AxiosResponse = await api.post('/chat/message', data);
    return response.data;
  },
  
  getChatHistory: async (sessionId: string) => {
    const response: AxiosResponse = await api.get(`/chat/history/${sessionId}`);
    return response.data;
  },
  
  getUserSessions: async () => {
    const response: AxiosResponse = await api.get('/chat/sessions');
    return response.data;
  },
};

// Agents API
export const agentsAPI = {
  getCapabilities: async () => {
    const response: AxiosResponse = await api.get('/agents/capabilities');
    return response.data;
  },
  
  getHealth: async () => {
    const response: AxiosResponse = await api.get('/agents/health');
    return response.data;
  },
  
  listAgents: async () => {
    const response: AxiosResponse = await api.get('/agents/list');
    return response.data;
  },
};

export default api;