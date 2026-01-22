import React, { useState } from "react";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import FileUpload from "./components/FileUpload";
import ScriptDisplay from "./components/ScriptDisplay";
import "./App.css"; // optional global resets

export default function App() {
  const [script, setScript] = useState("");
  const [scriptType, setScriptType] = useState("bash");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileUpload = async (file) => {
    setError("");
    setScript("");
    if (!file) {
      setError("No file selected.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", scriptType);

    try {
      setLoading(true);
      const res = await fetch("http://127.0.0.1:8000/generate-script/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setScript(data.script || "");
    } catch (err) {
      setError(err.message || "Unexpected error.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <Navbar />
      <Hero scriptType={scriptType} setScriptType={setScriptType} />

      <main className="main-content">
        <FileUpload onFileUpload={handleFileUpload} />
        {loading && <div className="muted">Generating script…</div>}
        {error && <div className="error-box">{error}</div>}
        <ScriptDisplay script={script} />
      </main>

      <footer className="footer">
        © 2026 Smart Environment Setup Assistant • Backend at <code>127.0.0.1:8000</code>
      </footer>
    </div>
  );
}