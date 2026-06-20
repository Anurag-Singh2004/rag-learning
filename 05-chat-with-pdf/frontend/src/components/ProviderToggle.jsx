export default function ProviderToggle({provider, setProvider}){
    return (
      <div
        className="inline-flex rounded-sm border text-xs"
        style={{ borderColor: "var(--rule)", fontFamily: "var(--font-mono)" }}
      >
        {["groq", "gemini"].map((p) => (
          <button
            key={p}
            onClick={() => setProvider(p)}
            className="px-3 py-1.5 transition-colors"
            style={{
              background: provider === p ? "var(--evidence)" : "transparent",
              color: provider === p ? "#FAF8F3" : "var(--ink-soft)",
            }}
          >
            {p}
          </button>
        ))}
      </div>
    );
}