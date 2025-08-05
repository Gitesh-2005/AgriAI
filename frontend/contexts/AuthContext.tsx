import React, {
  createContext,
  useState,
  useContext,
  useCallback,
  useEffect,
} from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

interface User {
  id: number;
  email: string;
  full_name: string;
  user_type: string;
  language_preference: string;
  location?: string;
  farm_size?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: any) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }

    setIsLoading(false);
  }, []);

  const login = useCallback(
    async (email: string, password: string) => {
      try {
        setIsLoading(true);
        const response = await axios.post(
          'http://localhost:8000/api/v1/auth/login',
          { email, password }
        );

        const { access_token } = response.data;
        setToken(access_token);
        localStorage.setItem('token', access_token);

        const userInfo = await axios.get(
          'http://localhost:8000/api/v1/auth/users/me',
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          }
        );

        setUser(userInfo.data);
        localStorage.setItem('user', JSON.stringify(userInfo.data));

        toast.success('Login successful!');
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Login failed');
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const register = useCallback(
    async (userData: any) => {
      try {
        setIsLoading(true);
        const response = await axios.post(
          'http://localhost:8000/api/v1/auth/register',
          userData
        );

        const { access_token } = response.data;
        setToken(access_token);
        localStorage.setItem('token', access_token);

        const userInfo = await axios.get(
          'http://localhost:8000/api/v1/auth/users/me',
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          }
        );

        setUser(userInfo.data);
        localStorage.setItem('user', JSON.stringify(userInfo.data));

        toast.success('Registration successful!');
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Registration failed');
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const logout = useCallback(() => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    toast.success('Logged out successfully');
  }, []);

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!user && !!token,
    login,
    register,
    logout,
    isLoading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
