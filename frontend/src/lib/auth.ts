// src/lib/auth.ts
export type AuthUser = { id: string; email: string; name: string };
type StoredUser = AuthUser & { password: string };

const LS_USERS = "mi_tienda_users";
const LS_TOKEN = "mi_tienda_token";
const LS_ME = "mi_tienda_me";

// --- helpers de almacenamiento ---
function readUsers(): StoredUser[] {
  const raw = localStorage.getItem(LS_USERS);
  return raw ? JSON.parse(raw) : [];
}
function writeUsers(users: StoredUser[]) {
  localStorage.setItem(LS_USERS, JSON.stringify(users));
}

// --- FAKE backend (puedes reemplazar por fetch a tu API) ---
async function fakeRegister(name: string, email: string, password: string) {
  const users = readUsers();
  if (users.some(u => u.email === email)) {
    throw new Error("Ya existe un usuario con ese email");
  }
  const newUser: StoredUser = {
    id: crypto.randomUUID(),
    name,
    email,
    password,
  };
  users.push(newUser);
  writeUsers(users);

  // token ultra simple
  const token = `${newUser.id}.${Date.now()}`;
  localStorage.setItem(LS_TOKEN, token);
  localStorage.setItem(LS_ME, JSON.stringify({ id: newUser.id, name, email }));
  return { token, user: { id: newUser.id, name, email } as AuthUser };
}

async function fakeLogin(email: string, password: string) {
  const users = readUsers();
  const found = users.find(u => u.email === email && u.password === password);
  if (!found) throw new Error("Credenciales inválidas");
  const token = `${found.id}.${Date.now()}`;
  localStorage.setItem(LS_TOKEN, token);
  localStorage.setItem(
    LS_ME,
    JSON.stringify({ id: found.id, name: found.name, email: found.email })
  );
  return {
    token,
    user: { id: found.id, name: found.name, email: found.email } as AuthUser,
  };
}

// --- API pública que usa el resto de la app ---
export async function register(name: string, email: string, password: string) {
  // reemplaza por: return fetch('/api/register', { ... })
  return fakeRegister(name, email, password);
}

export async function login(email: string, password: string) {
  // reemplaza por: return fetch('/api/login', { ... })
  return fakeLogin(email, password);
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
