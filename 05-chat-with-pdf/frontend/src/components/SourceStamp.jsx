import { useState } from "react";

export default function SourceStamp({ chunksUsed, sources }) {
  const [expanded, setExpanded] = useState(false);

  if (chunksUsed === 0) {
    return (
      <span
        className="mt-2 text-xs px-2 py-1 rounded-sm inline-block"
        style={{
          fontFamily: "var(--font-mono)",
          background: "#EFEDE6",
          color: "var(--ink-soft)",
        }}
      >
        no source · context not found
      </span>
    );
  }

  return (
    <div className="mt-2">
      <button
        onClick={() => setExpanded((v) => !v)}
        className="text-xs px-2 py-1 rounded-sm border inline-flex items-center gap-1.5"
        style={{
          fontFamily: "var(--font-mono)",
          borderColor: "var(--stamp)",
          color: "var(--stamp)",
        }}
      >
        <span style={{ fontWeight: 600 }}>sourced</span>
        <span>
          · {chunksUsed} chunk{chunksUsed !== 1 ? "s" : ""}
        </span>
        <span>{expanded ? "−" : "+"}</span>
      </button>

      {expanded && (
        <div className="mt-2 space-y-2">
          {sources.map((s, i) => (
            <div
              key={i}
              className="text-xs px-3 py-2 rounded-sm border"
              style={{
                fontFamily: "var(--font-mono)",
                borderColor: "var(--rule)",
                background: "#FFFFFF",
                color: "var(--ink-soft)",
              }}
            >
              {s}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
