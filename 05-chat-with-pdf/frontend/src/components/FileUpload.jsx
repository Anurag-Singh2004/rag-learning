import { useState, useRef } from "react";

export default function FileUpload({onUploadComplete, uploadedFiles}){
  const [isDragging, setIsDragging] = useState(false);
  const [status, setStatus] = useState("idle"); // idle | uploading | error
  const [error, setError] = useState('')
  const inputRef = useRef(null) //important

  async function handleFile(file){
    if(!file || file.type !== 'application/pdf'){
        setStatus('error')
        setError('Only PDF files are accepted')
        return
    }
    setStatus('uploading')
    setError('')

    const formData = new FormData() //used for sending pdf or images or files etc to backend since we cannot use json for these formats.
    formData.append('file', file)

    try{
        const res = await fetch('/api/upload',{
            method: 'POST',
            body: formData,
        });
        if(!res.ok) throw new Error(`Upload failed (${res.status})`)
        const data = await res.json();
        onUploadComplete({
          filename: data.filename,
          chunks: data.chunks_created,
        });
        setStatus('idle')
    }catch(err){
        setStatus('error')
        setError(err.message || "Something went wrong during upload.");
    }
  }
  return (
    <div className="flex flex-col h-full">
      <div
        className="px-5 pt-6 pb-4 border-b"
        style={{ borderColor: "var(--rule)" }}
      >
        <p
          className="text-xs tracking-widest uppercase mb-1"
          style={{ fontFamily: "var(--font-mono)", color: "var(--ink-soft)" }}
        >
          Case File
        </p>
        <h1
          className="text-2xl leading-tight"
          style={{ fontFamily: "var(--font-display)", color: "var(--ink)" }}
        >
          Document Examiner
        </h1>
      </div>

      <div className="px-5 py-5 flex-1">
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setIsDragging(false);
            handleFile(e.dataTransfer.files?.[0]);
          }}
          onClick={() => inputRef.current?.click()}
          className="cursor-pointer rounded-sm border-2 border-dashed px-4 py-10 text-center transition-colors"
          style={{
            borderColor: isDragging ? "var(--evidence)" : "var(--rule)",
            background: isDragging ? "var(--evidence-soft)" : "transparent",
          }}
        >
          <input
            ref={inputRef}
            type="file"
            accept="application/pdf"
            className="hidden"
            onChange={(e) => handleFile(e.target.files?.[0])}
          />
          {status === "uploading" ? (
            <p className="text-sm" style={{ color: "var(--ink-soft)" }}>
              Processing document…
            </p>
          ) : (
            <>
              <p className="text-sm mb-1" style={{ color: "var(--ink)" }}>
                Drop a PDF here, or click to browse
              </p>
              <p className="text-xs" style={{ color: "var(--ink-soft)" }}>
                One file at a time, added to the case
              </p>
            </>
          )}
        </div>
        {status === "error" && (
          <p
            className="mt-3 text-xs px-3 py-2 rounded-sm"
            style={{
              background: "#FBEAE5",
              color: "#A03B2A",
              fontFamily: "var(--font-mono)",
            }}
          >
            {error}
          </p>
        )}

        {uploadedFiles.length > 0 && (
          <div className="mt-6">
            <p
              className="text-xs tracking-widest uppercase mb-2"
              style={{
                fontFamily: "var(--font-mono)",
                color: "var(--ink-soft)",
              }}
            >
              Entered into evidence
            </p>
            <ul className="space-y-2">
              {uploadedFiles.map((f, i) => (
                <li
                  key={i}
                  className="text-xs px-3 py-2 rounded-sm border flex justify-between gap-2"
                  style={{
                    borderColor: "var(--rule)",
                    fontFamily: "var(--font-mono)",
                  }}
                >
                  <span className="truncate" title={f.filename}>
                    {f.filename}
                  </span>
                  <span style={{ color: "var(--ink-soft)" }}>{f.chunks}c</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}