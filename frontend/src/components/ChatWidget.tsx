import { useEffect, useRef, useState } from "react";
import { api } from "../lib/api";
import type { ChatMessage } from "../lib/types";

export default function ChatWidget() {
  // Estado tipado explícito
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "¡Hola! Soy tu estilista virtual 👗 ¿Buscas zapatos, vestidos o algo para una ocasión especial?",
    },
  ]);

  const boxRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    boxRef.current?.scrollTo({ top: 1e9, behavior: "smooth" });
  }, [messages, open]);

  const send = async (text: string) => {
    const clean = text.trim();
    if (!clean) return;

    // Construimos mensajes con tipo ChatMessage
    const userMsg: ChatMessage = { role: "user", content: clean };
    const next: ChatMessage[] = [...messages, userMsg];

    setMessages(next);
    setLoading(true);

    try {
      const { reply } = await api.chat(next);
      const assistantMsg: ChatMessage = { role: "assistant", content: reply };
      setMessages([...next, assistantMsg]);
    } catch {
      const errMsg: ChatMessage = {
        role: "assistant",
        content: "Ups, hubo un error. Intenta más tarde.",
      };
      setMessages([...next, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  const sendFromInput = () => {
    const input = document.querySelector<HTMLInputElement>(
      'input[data-chat-input="true"]'
    );
    if (input) {
      const v = input.value;
      input.value = "";
      send(v);
    }
  };

  return (
    <>
      {/* Botón flotante */}
      <button
        onClick={() => setOpen(!open)}
        className="fixed bottom-4 right-4 z-40 rounded-full w-14 h-14 shadow-lg bg-black text-white"
        aria-label="Abrir chat"
        title="Chat"
      >
        💬
      </button>

      {/* Ventana de chat */}
      {open && (
        <div className="fixed bottom-20 right-4 z-40 w-80 max-h-[70vh] bg-white shadow-2xl rounded-2xl overflow-hidden flex flex-col">
          <div className="px-3 py-2 border-b font-semibold">Asistente</div>

          <div ref={boxRef} className="flex-1 p-3 space-y-2 overflow-auto">
            {messages.map((m, i) => (
              <div
                key={i}
                className={`px-3 py-2 rounded-xl max-w-[85%] ${
                  m.role === "user"
                    ? "bg-black text-white ml-auto"
                    : "bg-gray-100"
                }`}
              >
                {m.content}
              </div>
            ))}
            {loading && (
              <div className="text-sm text-gray-500">Escribiendo…</div>
            )}
          </div>

          <div className="p-2 border-t flex gap-2">
            <input
              data-chat-input="true"
              className="flex-1 border rounded-xl px-3 py-2"
              placeholder="Pregunta por tallas, estilos…"
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  const el = e.currentTarget;
                  const v = el.value;
                  el.value = "";
                  send(v);
                }
              }}
            />
            <button
              onClick={sendFromInput}
              className="px-3 py-2 rounded-xl bg-black text-white"
            >
              Enviar
            </button>
          </div>
        </div>
      )}
    </>
  );
}
