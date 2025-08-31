import type { Category } from "../lib/types";

const CATS: { key: Category; label: string }[] = [
  { key: 'zapatos', label: 'Zapatos' },
  { key: 'pantalones', label: 'Pantalones' },
  { key: 'vestidos', label: 'Vestidos' },
  { key: 'blusas', label: 'Blusas' },
  { key: 'accesorios', label: 'Accesorios' },
];

export default function Navbar({
  active, onChange, onOpenCart
}:{ active: Category|'todas'; onChange:(c:Category|'todas')=>void; onOpenCart:()=>void }) {
  return (
    <header className="sticky top-0 z-20 bg-white/90 backdrop-blur border-b">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <a href="#" className="font-bold text-xl">Aurora</a>
        <nav className="hidden md:flex items-center gap-4 text-sm">
          <button className={`px-3 py-1 rounded-lg ${active==='todas'?'bg-black text-white':'hover:bg-gray-100'}`} onClick={()=>onChange('todas')}>Todas</button>
          {CATS.map(c=>(
            <button key={c.key}
              className={`px-3 py-1 rounded-lg ${active===c.key?'bg-black text-white':'hover:bg-gray-100'}`}
              onClick={()=>onChange(c.key)}>{c.label}</button>
          ))}
        </nav>
        <button onClick={onOpenCart} className="rounded-xl border px-3 py-2 text-sm">🛒 Carrito</button>
      </div>

      {/* Nav móvil */}
      <div className="md:hidden border-t">
        <div className="max-w-6xl mx-auto px-4 py-2 flex gap-2 overflow-auto">
          <button className={`px-3 py-1 rounded-lg ${active==='todas'?'bg-black text-white':'bg-gray-100'}`} onClick={()=>onChange('todas')}>Todas</button>
          {CATS.map(c=>(
            <button key={c.key} className={`px-3 py-1 rounded-lg ${active===c.key?'bg-black text-white':'bg-gray-100'}`} onClick={()=>onChange(c.key)}>{c.label}</button>
          ))}
        </div>
      </div>
    </header>
  );
}
