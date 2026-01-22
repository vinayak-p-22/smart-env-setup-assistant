import React from "react";
import "./ScriptDisplay.css";
export default function ScriptDisplay({ script }) {
  if (!script) return <div className="muted">No script yet. Upload a Requirements.txt file for gerating script</div>;
  return (
    <div className="script-view">
      <pre className="script-pre">{script}</pre>
    </div>
  );
}