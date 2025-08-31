import type { Product } from "../lib/types";

const fmtCLP = new Intl.NumberFormat("es-CL", {
  style: "currency",
  currency: "CLP",
  minimumFractionDigits: 0,
});

export default function ProductCard({
  p,
  onAdd,
}: {
  p: Product;
  onAdd: (p: Product) => void;
}) {
  const price = fmtCLP.format(p.priceCents);

  return (
    <div className="bg-white rounded-2xl shadow p-3 flex flex-col">
      <img
        src={p.imageUrl || "https://via.placeholder.com/600x400"}
        alt={p.name}
        className="rounded-xl mb-3 h-80 w-full object-cover"
      />
      <h3 className="font-semibold">{p.name}</h3>
      {p.description && (
        <p className="text-sm text-gray-600">{p.description}</p>
      )}
      <div className="mt-auto flex items-center justify-between pt-3">
        <span className="font-bold">{price}</span>
        <button
          onClick={() => onAdd(p)}
          className="px-3 py-2 rounded-xl bg-black text-white hover:opacity-90"
        >
          Agregar
        </button>
      </div>
    </div>
  );
}
