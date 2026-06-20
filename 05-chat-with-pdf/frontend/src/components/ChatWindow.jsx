import { useState, useRef, useEffect } from "react";
import MessageBubble from "./MessageBubble";
import ProviderToggle from "./ProviderToggle";

export default function ChatWindow({ hasDocument }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [provider, setProvider] = useState("groq");
  const [isThinking, setIsThinking] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  async function sendMessage() {
    const question = input.trim();
    if (!question || isThinking) return;

    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setInput("");
    setIsThinking(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, provider }),
      });
      if (!res.ok) throw new Error(`Request failed (${res.status})`);
      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          chunksUsed: data.chunks_used,
          sources: data.sources,
          provider,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Couldn't reach the examiner. ${err.message}`,
          chunksUsed: 0,
          provider,
        },
      ]);
    } finally {
      setIsThinking(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div
        className="px-6 py-4 border-b flex items-center justify-between"
        style={{ borderColor: "var(--rule)" }}
      >
        <p
          className="text-xs tracking-widest uppercase"
          style={{ fontFamily: "var(--font-mono)", color: "var(--ink-soft)" }}
        >
          Transcript
        </p>
        <ProviderToggle provider={provider} setProvider={setProvider} />
      </div>

      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-5">
        {messages.length === 0 && (
          <div className="h-full flex items-center justify-center text-center">
            <p
              className="text-sm max-w-xs"
              style={{ color: "var(--ink-soft)" }}
            >
              {hasDocument
                ? "Ask a question about the document on file."
                : "Upload a document on the left to open the case."}
            </p>
          </div>
        )}

        {messages.map((m, i) => (
          <MessageBubble key={i} {...m} />
        ))}

        {isThinking && (
          <div className="flex justify-start">
            <p
              className="text-xs px-4 py-3"
              style={{
                fontFamily: "var(--font-mono)",
                color: "var(--ink-soft)",
              }}
            >
              examining record…
            </p>
          </div>
        )}
        <div ref={scrollRef} />
      </div>

      <div
        className="px-6 py-4 border-t"
        style={{ borderColor: "var(--rule)" }}
      >
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={!hasDocument}
            placeholder={
              hasDocument
                ? "Ask about the document…"
                : "Upload a document first"
            }
            className="flex-1 px-4 py-2.5 rounded-sm border text-sm outline-none"
            style={{ borderColor: "var(--rule)", background: "#FFFFFF" }}
          />
          <button
            onClick={sendMessage}
            disabled={!hasDocument || isThinking}
            className="px-5 py-2.5 rounded-sm text-sm font-medium disabled:opacity-40"
            style={{ background: "var(--ink)", color: "var(--paper)" }}
          >
            Ask
          </button>
        </div>
      </div>
    </div>
  );
}
