import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Link, useNavigate } from "react-router-dom";

export default function Register() {
  const { register } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const navigate = useNavigate();

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      setErr(null);
      await register(name, email, password);
      navigate("/", { replace: true });
    } catch (e: any) {
      setErr(e.message ?? "Error inesperado");
    }
  }

  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Crear cuenta</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input className="w-full border rounded p-2" placeholder="Nombre" value={name} onChange={e=>setName(e.target.value)} required />
        <input className="w-full border rounded p-2" type="email" placeholder="Correo" value={email} onChange={e=>setEmail(e.target.value)} required />
        <input className="w-full border rounded p-2" type="password" placeholder="Contraseña" value={password} onChange={e=>setPassword(e.target.value)} required minLength={6} />
        {err && <p className="text-red-600 text-sm">{err}</p>}
        <button className="w-full bg-black text-white rounded p-2">Registrarme</button>
      </form>
      <p className="mt-4 text-sm">¿Ya tienes cuenta? <Link className="underline" to="/login">Inicia sesión</Link></p>
    </div>
  );
}
