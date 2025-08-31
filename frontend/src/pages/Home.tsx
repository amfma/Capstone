import { useEffect, useMemo, useState } from "react";
import type { Product, Category } from "../lib/types";
import { api } from "../lib/api";
import ProductCard from "../components/ProductCard";

export default function Home({
  active, onAdd
}:{ active: Category|'todas'; onAdd:(p:Product)=>void }){
  const [items, setItems] = useState<Product[]>([]);
  const [err, setErr] = useState<string>();

  useEffect(()=>{ api.listProducts().then(setItems).catch(e=>setErr(e.message)); },[]);
  const filtered = useMemo(()=> active==='todas' ? items : items.filter(p=>p.category===active), [items, active]);

  if (err) return <div className="max-w-6xl mx-auto px-4 py-6 text-red-600">Error cargando productos: {err}</div>;

  return (
    <main className="max-w-6xl mx-auto px-4 py-6">
      <section className="mb-8">
        <div className="rounded-2xl bg-gradient-to-r from-fuchsia-600 to-rose-500 text-white p-8">
          <h1 className="text-3xl font-bold">Nueva Colección Mujer ✨</h1>
          <p className="mt-2 text-white/90">Zapatos, pantalones, vestidos, blusas y accesorios.</p>
          <button className="mt-4 px-4 py-2 rounded-xl bg-white text-black text-sm">Ver catálogo</button>
        </div>
      </section>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {filtered.map(p => <ProductCard key={p.id} p={p} onAdd={onAdd} />)}
      </div>
    </main>
  );
}
