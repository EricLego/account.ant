import React from "react";
import "./TopBar.css";

const TopBar = () => {
  const userName = localStorage.getItem("name") || "User";

  return (
    <header className="top-bar">
      <h1 className="top-bar-title">Home</h1>
      <div className="top-bar-user">
        <span>Welcome, {userName}</span>
      </div>
    </header>
  );
};

export default TopBar;
