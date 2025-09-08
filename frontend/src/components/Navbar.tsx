import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import type { Category } from "../lib/types";

const CATS: { key: Category; label: string }[] = [
  { key: "zapatos", label: "Zapatos" },
  { key: "pantalones", label: "Pantalones" },
  { key: "vestidos", label: "Vestidos" },
  { key: "blusas", label: "Blusas" },
  { key: "accesorios", label: "Accesorios" },
];

export default function Navbar({
  active, onChange, onOpenCart
}:{ active: Category|'todas'; onChange:(c:Category|'todas')=>void; onOpenCart:()=>void }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/", { replace: true });
  };

  return (
    <header className="sticky top-0 z-20 bg-white/90 backdrop-blur border-b">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="font-bold text-xl">Aurora</Link>

        <nav className="hidden md:flex items-center gap-4 text-sm">
          <button className={`px-3 py-1 rounded-lg ${active==='todas'?'bg-black text-white':'hover:bg-gray-100'}`} onClick={()=>onChange('todas')}>Todas</button>
          {CATS.map(c=>(
            <button key={c.key}
              className={`px-3 py-1 rounded-lg ${active===c.key?'bg-black text-white':'hover:bg-gray-100'}`}
              onClick={()=>onChange(c.key)}>{c.label}</button>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          {user ? (
            <>
              <span className="hidden sm:inline text-sm text-gray-600">Hola, {user.name.split(" ")[0]}</span>
              <button onClick={handleLogout} className="text-sm underline underline-offset-2 hover:text-black">Salir</button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm underline underline-offset-2 hover:text-black">Entrar</Link>
              <Link to="/register" className="text-sm underline underline-offset-2 hover:text-black">Registrarse</Link>
            </>
          )}
          <button onClick={onOpenCart} className="rounded-xl border px-3 py-2 text-sm" aria-label="Abrir carrito">🛒 Carrito</button>
        </div>
      </div>

      {/* móvil */}
      <div className="md:hidden border-t">
        <div className="max-w-6xl mx-auto px-4 py-2 flex gap-2 overflow-auto">
          <button className={`px-3 py-1 rounded-lg ${active==='todas'?'bg-black text-white':'bg-gray-100'}`} onClick={()=>onChange('todas')}>Todas</button>
          {CATS.map(c=>(
            <button key={c.key} className={`px-3 py-1 rounded-lg ${active===c.key?'bg-black text-white':'bg-gray-100'}`} onClick={()=>onChange(c.key)}>{c.label}</button>
          ))}
        </div>
        <div className="max-w-6xl mx-auto px-4 pb-3 flex items-center justify-end gap-3">
          {user ? (
            <>
              <span className="text-sm text-gray-600">Hola, {user.name.split(" ")[0]}</span>
              <button onClick={handleLogout} className="text-sm underline underline-offset-2 hover:text-black">Salir</button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm underline underline-offset-2">Entrar</Link>
              <Link to="/register" className="text-sm underline underline-offset-2">Registrarse</Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
