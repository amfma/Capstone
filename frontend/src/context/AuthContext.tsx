import React, { createContext, useContext, useEffect, useState } from "react";

export type AuthUser = { id: string; email: string; name: string };

const LS_TOKEN = "mi_tienda_token";
const LS_ME = "mi_tienda_me";

function getCurrentUser(): AuthUser | null {
  const raw = localStorage.getItem(LS_ME);
  return raw ? (JSON.parse(raw) as AuthUser) : null;
}

async function fakeLogin(email: string, _password: string) {
  const user = getCurrentUser() ?? { id: crypto.randomUUID(), name: "Invitado", email };
  localStorage.setItem(LS_TOKEN, "demo." + Date.now());
  localStorage.setItem(LS_ME, JSON.stringify(user));
  return { user };
}

async function fakeRegister(name: string, email: string, _password: string) {
  const user = { id: crypto.randomUUID(), name, email };
  localStorage.setItem(LS_TOKEN, "demo." + Date.now());
  localStorage.setItem(LS_ME, JSON.stringify(user));
  return { user };
}

function logoutLS() {
  localStorage.removeItem(LS_TOKEN);
  localStorage.removeItem(LS_ME);
}

type AuthContextType = {
  user: AuthUser | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setUser(getCurrentUser());
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    const res = await fakeLogin(email, password);
    setUser(res.user);
  };
  const register = async (name: string, email: string, password: string) => {
    const res = await fakeRegister(name, email, password);
    setUser(res.user);
  };
  const logout = () => {
    logoutLS();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth debe usarse dentro de <AuthProvider>");
  return ctx;
}
