import { createContext, useCallback, useContext, useMemo, useState } from 'react';
import type { ReactNode } from 'react';

type AuthContextType = {
  token: string | null;
  setToken: (token: string | null) => void;
  isAuthenticated: boolean;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

let currentToken: string | null = null;

export const authTokenStore = {
  getToken: () => currentToken
};

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenState] = useState<string | null>(null);

  const setToken = useCallback((nextToken: string | null) => {
    currentToken = nextToken;
    setTokenState(nextToken);
  }, []);

  const value = useMemo(
    () => ({
      token,
      setToken,
      isAuthenticated: Boolean(token)
    }),
    [token, setToken]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
