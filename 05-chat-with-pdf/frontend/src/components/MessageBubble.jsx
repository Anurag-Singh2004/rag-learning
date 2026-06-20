import SourceStamp from "./SourceStamp";

export default function MessageBubble({
  role,
  content,
  chunksUsed,
  sources,
  provider,
}) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className="max-w-[75%]">
        <p
          className="text-[10px] tracking-widest uppercase mb-1"
          style={{
            fontFamily: "var(--font-mono)",
            color: "var(--ink-soft)",
            textAlign: isUser ? "right" : "left",
          }}
        >
          {isUser ? "You" : `Witness (${provider})`}
        </p>
        <div
          className="px-4 py-3 rounded-sm text-sm leading-relaxed"
          style={{
            background: isUser ? "var(--evidence)" : "#FFFFFF",
            color: isUser ? "#FAF8F3" : "var(--ink)",
            border: isUser ? "none" : "1px solid var(--rule)",
          }}
        >
          {content}
        </div>
        {!isUser && (
          <SourceStamp chunksUsed={chunksUsed} sources={sources || []} />
        )}
      </div>
    </div>
  );
}
