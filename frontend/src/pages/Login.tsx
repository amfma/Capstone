import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Link, useLocation, useNavigate } from "react-router-dom";

export default function Login() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const navigate = useNavigate();
  const location = useLocation() as any;
  const from = location.state?.from?.pathname || "/";

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      setErr(null);
      await login(email, password);
      navigate(from, { replace: true });
    } catch (e: any) {
      setErr(e.message ?? "Error inesperado");
    }
  }

  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Iniciar sesión</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input className="w-full border rounded p-2" type="email" placeholder="Correo" value={email} onChange={e=>setEmail(e.target.value)} required />
        <input className="w-full border rounded p-2" type="password" placeholder="Contraseña" value={password} onChange={e=>setPassword(e.target.value)} required />
        {err && <p className="text-red-600 text-sm">{err}</p>}
        <button className="w-full bg-black text-white rounded p-2">Entrar</button>
      </form>
      <p className="mt-4 text-sm">¿No tienes cuenta? <Link className="underline" to="/register">Regístrate</Link></p>
    </div>
  );
}
