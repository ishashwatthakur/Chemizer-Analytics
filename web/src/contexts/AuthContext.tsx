import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { apiClient } from '../lib/api';

interface User {
  user_id: string | number;
  username: string;
  email: string;
  full_name?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (token: string, userData: User) => void;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);
const SESSION_TIMEOUT_MS = 48 * 60 * 60 * 1000; // 48 hours

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check session expiration
  useEffect(() => {
    const storedToken = apiClient.getToken();
    const storedUser = apiClient.getUserData();
    const loginTime = localStorage.getItem('login_timestamp');

    if (storedToken && storedUser && loginTime) {
      const currentTime = Date.now();
      const elapsed = currentTime - parseInt(loginTime);

      if (elapsed < SESSION_TIMEOUT_MS) {
        setToken(storedToken);
        setUser(storedUser);
      } else {
        // Session expired
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_data');
        localStorage.removeItem('login_timestamp');
        localStorage.setItem('isAuthenticated', 'false');
        apiClient.logout();
      }
    }
    setIsLoading(false);
  }, []);

  const login = (newToken: string, userData: User) => {
    setToken(newToken);
    setUser(userData);
    apiClient.setToken(newToken);
    apiClient.setUserData(userData);
    localStorage.setItem('login_timestamp', Date.now().toString());
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    apiClient.logout();
    localStorage.removeItem('login_timestamp');
  };

  const updateUser = (userData: Partial<User>) => {
    if (user) {
      const updatedUser = { ...user, ...userData };
      setUser(updatedUser);
      apiClient.setUserData(updatedUser);
    }
  };

  const value = {
    user,
    token,
    isAuthenticated: !!token,
    isLoading,
    login,
    logout,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
