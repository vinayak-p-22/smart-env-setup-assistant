import React from "react";
import "./Hero.css";
export default function Hero({ scriptType, setScriptType }) {
  return (
    <section className="hero">
      <h1 className="hero-title">Smart Environment Setup Assistant</h1>
      <p className="hero-sub">
        Upload your dependency file and instantly generate Bash, PowerShell, or Docker setup scripts.
      </p>
      <div className="segmented">
        <button
          className={scriptType === "bash" ? "seg-btn active" : "seg-btn"}
          onClick={() => setScriptType("bash")}
        >
          Bash
        </button>
        <button
          className={scriptType === "powershell" ? "seg-btn active" : "seg-btn"}
          onClick={() => setScriptType("powershell")}
        >
          PowerShell
        </button>
        <button
          className={scriptType === "docker" ? "seg-btn active" : "seg-btn"}
          onClick={() => setScriptType("docker")}
        >
          Dockerfile
        </button>
      </div>
    </section>
  );
}