import React from "react";
import "./TopBar.css";
import { FaUser } from "react-icons/fa";

const TopBar = ({ title = "Dashboard" }) => {
  const userName = localStorage.getItem("name") || "User";
  const profilePicture = localStorage.getItem("profilePicture") || "/default-profile.jpg";

  return (
    <header className="top-bar">
      <h1 className="top-bar-title">{title}</h1>
      <div className="top-bar-user">
        <span className="user-name">Welcome, {userName}</span>
        <img className="user-profile" src={profilePicture} alt="Profile" />
      </div>
    </header>
  );
};

export default TopBar;
