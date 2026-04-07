/**
 * Auth Context — React context provider for authentication state.
 * Provides login(), logout(), register() actions.
 */

"use client";

import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import {
  api,
  setAccessToken,
  setRefreshToken,
  getAccessToken,
  type TokenResponse,
} from "@/lib/api";

interface AuthUser {
  id: string;
  email: string;
  name: string;
  role: string;
}

interface AuthContextType {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  login: async () => {},
  register: async () => {},
  logout: () => {},
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check for existing session on mount
  useEffect(() => {
    const token = getAccessToken();
    if (token) {
      api.auth
        .me()
        .then((userData) => {
          setUser(userData);
        })
        .catch(() => {
          setAccessToken(null);
          setRefreshToken(null);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const handleTokens = useCallback((tokens: TokenResponse) => {
    setAccessToken(tokens.access_token);
    setRefreshToken(tokens.refresh_token);
  }, []);

  const login = useCallback(
    async (email: string, password: string) => {
      const tokens = await api.auth.login(email, password);
      handleTokens(tokens);
      const userData = await api.auth.me();
      setUser(userData);
    },
    [handleTokens]
  );

  const register = useCallback(
    async (email: string, password: string, name: string) => {
      const tokens = await api.auth.register(email, password, name);
      handleTokens(tokens);
      const userData = await api.auth.me();
      setUser(userData);
    },
    [handleTokens]
  );

  const logout = useCallback(() => {
    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);
    if (typeof window !== "undefined") {
      window.location.href = "/";
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
