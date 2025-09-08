import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Link, useNavigate } from "react-router-dom";
import axios, { formToJSON } from "axios";
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

export default function Register() {
  const { register } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(false)

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    const formData = new FormData()
    formData.append('email', email)
    formData.append('nombres', name)
    formData.append('apellidos', 'difussion')
    formData.append('password', password)
    try {
      await axios.post('http://localhost:8000/api/v1/usuarios', formToJSON(formData), {
        headers: { 'Content-Type': 'application/json'}
      });
      handleOpen()
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
        <button type='submit' className="w-full bg-black text-white rounded p-2">Registrarme</button>
      </form>
      <p className="mt-4 text-sm">¿Ya tienes cuenta? <Link className="underline" to="/login">Inicia sesión</Link></p>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {"Usuario creado"}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Usuario creado apropiadamente
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Ok</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
