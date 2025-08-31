export type Category = 'zapatos' | 'pantalones' | 'vestidos' | 'blusas' | 'accesorios';

export type Product = {
  id: number;
  name: string;
  description?: string;
  priceCents: number;
  imageUrl?: string;
  category: Category;
};

export type CheckoutItem = { name: string; priceCents: number; qty: number };
export type ChatMessage = { role: 'user'|'assistant'|'system'; content: string };
