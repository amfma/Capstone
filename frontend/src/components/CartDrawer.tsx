import type { Product } from "../lib/types";

type Item = Product & { qty: number };

const fmtCLP = new Intl.NumberFormat("es-CL", {
  style: "currency",
  currency: "CLP",
  minimumFractionDigits: 0,
});

export default function CartDrawer({
  open,
  onClose,
  items,
  onInc,
  onDec,
  onClear,
  onCheckout,
}: {
  open: boolean;
  onClose: () => void;
  items: Item[];
  onInc: (id: number) => void;
  onDec: (id: number) => void;
  onClear: () => void;
  onCheckout: () => void;
}) {
  if (!open) return null;

  // Total en CLP (nuestros priceCents ya están en CLP, ¡no dividir por 100!)
  const total = items.reduce((a, i) => a + i.priceCents * i.qty, 0);

  return (
    <div className="fixed inset-0 z-30">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />
      <aside className="absolute right-0 top-0 h-full w-full max-w-md bg-white shadow-xl p-4">
        <h2 className="text-lg font-semibold mb-2">Tu carrito</h2>

        <ul className="space-y-3">
          {items.map((i) => {
            const lineTotal = i.priceCents * i.qty;
            return (
              <li
                key={i.id}
                className="flex items-center justify-between border rounded-xl p-2"
              >
                <div>
                  <div className="font-medium">{i.name}</div>
                  <div className="text-sm text-gray-600">
                    {fmtCLP.format(i.priceCents)} × {i.qty} ={" "}
                    <strong>{fmtCLP.format(lineTotal)}</strong>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => onDec(i.id)}
                    className="px-2 py-1 border rounded"
                  >
                    -
                  </button>
                  <span>{i.qty}</span>
                  <button
                    onClick={() => onInc(i.id)}
                    className="px-2 py-1 border rounded"
                  >
                    +
                  </button>
                </div>
              </li>
            );
          })}
        </ul>

        <div className="mt-6 flex items-center justify-between">
          <span className="font-semibold">Total</span>
          <span className="font-bold">{fmtCLP.format(total)}</span>
        </div>

        <div className="mt-4 flex gap-2">
          <button
            onClick={onCheckout}
            className="flex-1 bg-black text-white rounded-xl py-2"
          >
            Pagar
          </button>
          <button onClick={onClear} className="flex-1 border rounded-xl py-2">
            Vaciar
          </button>
        </div>
      </aside>
    </div>
  );
}
