import React from "react";
import "./Navbar.css";
export default function Navbar() {
  return (
    <header className="navbar">
      <div className="nav-inner">
        <div className="brand">Smart Environment Assistant</div>
        {/* <nav className="nav-links">
          <a href="#" className="nav-link">Docs</a>
          <a href="#" className="nav-link">Examples</a>
          <a href="#" className="nav-link">About</a>
        </nav> */}
      </div>
    </header>
  );
}