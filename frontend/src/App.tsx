import { useState } from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import CartDrawer from "./components/CartDrawer";
import ChatWidget from "./components/ChatWidget";
import type { Product, Category } from "./lib/types";
import { api } from "./lib/api";

type Item = Product & { qty:number };

export default function App(){
  const [active, setActive] = useState<Category|'todas'>('todas');
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState<Item[]>([]);

  const add = (p:Product) => setItems(s=>{
    const ex = s.find(i=>i.id===p.id);
    return ex ? s.map(i=>i.id===p.id?{...i, qty:i.qty+1}:i) : [...s, {...p, qty:1}];
  });
  const inc = (id:number) => setItems(s=>s.map(i=>i.id===id?{...i, qty:i.qty+1}:i));
  const dec = (id:number) => setItems(s=>s.map(i=>i.id===id?{...i, qty:Math.max(1,i.qty-1)}:i));
  const clear = () => setItems([]);

  const checkout = async () => {
    const res = await api.createCheckoutSession(items.map(i=>({ name:i.name, priceCents:i.priceCents, qty:i.qty })));
    if (res.url) window.location.href = res.url;
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <Navbar active={active} onChange={setActive} onOpenCart={()=>setOpen(true)} />
      <Home active={active} onAdd={add} />
      <CartDrawer open={open} onClose={()=>setOpen(false)} items={items} onInc={inc} onDec={dec} onClear={clear} onCheckout={checkout}/>
      <ChatWidget />
      <footer className="mt-16 border-t">
        <div className="max-w-6xl mx-auto px-4 py-6 text-sm text-gray-600 flex items-center justify-between">
          <span>© {new Date().getFullYear()} Tienda Aurora </span>
          <div className="flex gap-4">
            <a href="#tiendas" className="hover:text-black">Nuestras Tiendas</a>
            <a href="#politicas" className="hover:text-black">Políticas</a>
            <a href="#envios" className="hover:text-black">Envíos</a>
            <a href="#contacto" className="hover:text-black">Contacto</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
