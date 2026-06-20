import { useState, useEffect } from "react";
import FileUpload from "./components/FileUpload";
import ChatWindow from "./components/ChatWindow";

function App(){
    const [uploadedFiles, setUplodadedFiles] = useState([]);

    useEffect(() => {
      fetch("/api/documents")
        .then((res) => res.json())
        .then((data) => setUplodadedFiles(data.documents));
    }, []);

    function handleUploadComplete(file){
        setUplodadedFiles((prev)=>[...prev, file]);
    }
    return (
      <div
        className="h-screen w-screen flex"
        style={{ background: "var(--paper)" }}
      >
        <aside
          className="w-[320px] shrink-0 border-r"
          style={{ borderColor: "var(--rule)" }}
        >
          <FileUpload
            onUploadComplete={handleUploadComplete}
            uploadedFiles={uploadedFiles}
          />
        </aside>
        <main className="flex-1 min-w-0">
          <ChatWindow hasDocument={uploadedFiles.length > 0} />
        </main>
      </div>
    );
}

export default App;