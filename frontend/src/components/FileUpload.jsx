import React, { useState } from "react";
import "./FileUpload.css"; 

export default function FileUpload({ onFileUpload }) {
  const [fileName, setFileName] = useState("");

  const handleChange = (e) => {
    const f = e.target.files[0];
    setFileName(f ? f.name : "");
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const input = document.getElementById("file-input");
    if (input && input.files[0]) onFileUpload(input.files[0]);
  };

  return (
    <form className="upload-form" onSubmit={handleSubmit}>
      <label className="file-drop" htmlFor="file-input">
        <input id="file-input" type="file" accept=".txt,.json,.toml" onChange={handleChange} />
        <div className="file-drop-inner">
          <div className="file-title">{fileName || "Choose a file"}</div>
        </div>
      </label>
      <button type="submit" className="btn primary">Generate Script</button>
    </form>
  );
}