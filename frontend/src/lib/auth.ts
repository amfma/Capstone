// src/lib/auth.ts
export type AuthUser = { id: string; email: string; name: string, lastname:String };

const LS_TOKEN = "mi_tienda_token";
const LS_ME = "mi_tienda_me";


// --- API pública que usa el resto de la app ---
export async function register(name: string, lastname:string, email: string, password: string) {
  // reemplaza por: return fetch('/api/register', { ... })
  const response = await fetch('http://localhost:8000/api/v1/usuarios', {
    method: "POST",
    headers: { 'Content-Type': 'application/json'},
    body: JSON.stringify({nombres: name, apellidos: lastname, email: email, password: password})
  })
  const data = await response.json()
  if(!data.status){
    throw new Error('Correo ya registrado')
  }
}

export async function login(email: string, password: string) {
  // reemplaza por: return fetch('/api/login', { ... })
  const response = await fetch('http://localhost:8000/api/v1/login/', {
    method: "POST",
    headers: { 'Content-Type': 'application/json'},
    body: JSON.stringify({email: email, password:password})
  })
  const data = await response.json()
  console.log(data)
  if(!data.token){
    throw new Error(data.mensaje)
  } else {
    localStorage.setItem(LS_TOKEN, data.token)
    localStorage.setItem(LS_ME, JSON.stringify({id:data.id, email:data.id}))
    return true
  }
}

export function logout() {
  localStorage.removeItem(LS_TOKEN);
  localStorage.removeItem(LS_ME);
}

export function getCurrentUser(): AuthUser | null {
  const raw = localStorage.getItem(LS_ME);
  return raw ? (JSON.parse(raw) as AuthUser) : null;
}

export function isAuthenticated() {
  return Boolean(localStorage.getItem(LS_TOKEN));
}
