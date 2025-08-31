import type { Product, CheckoutItem, ChatMessage } from "./types";
import { MOCK_PRODUCTS } from "../mock/products";

const BASE = import.meta.env.VITE_API_BASE as string;
const USE_MOCK = import.meta.env.VITE_USE_MOCK === "1";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`HTTP ${res.status} ${res.statusText} ${text}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  // Productos: usa mock si está activado o si falla el fetch real
  listProducts: async (): Promise<Product[]> => {
    if (USE_MOCK) return MOCK_PRODUCTS;
    try { return await request<Product[]>("/products"); }
    catch { console.warn("Fallo /products → usando MOCK"); return MOCK_PRODUCTS; }
  },

  // Checkout: si mock, simulamos
  createCheckoutSession: async (items: CheckoutItem[]) => {
    if (USE_MOCK) {
      console.warn("Checkout simulado (mock).");
      return { id: "mock_session", url: "about:blank" };
    }
    return request<{ id: string; url: string }>("/checkout/session", {
      method: "POST",
      body: JSON.stringify({ items }),
    });
  },

  // Chat: si mock, respuesta fija
  chat: async (messages: ChatMessage[]) => {
    if (USE_MOCK) {
      const last = messages[messages.length - 1]?.content ?? "";
      return { reply: `👗 (Demo) Buscas: "${last}". Cuando el backend esté listo, te daré recomendaciones reales.` };
    }
    return request<{ reply: string }>("/chat", {
      method: "POST",
      body: JSON.stringify({ messages }),
    });
  },
};
