import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api"; // Centralized Axios instance
import "./TopBar.css";
import { FaUser } from "react-icons/fa";

const TopBar = () => {
  const [userName, setUserName] = useState("User");
  const [profilePicture, setProfilePicture] = useState("/default-profile.jpg");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await api.post("/auth/validate", {
          token: localStorage.getItem("token"),
        });

        setUserName(response.data.name || "User");
        localStorage.setItem("name", response.data.name);

      } catch (err) {
        console.error("Token validation failed", err);
        localStorage.removeItem("token");
        navigate("/login"); // Redirect to login if token is invalid
      }
    };

    fetchUserData();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("name");
    localStorage.removeItem("profilePicture");
    navigate("/login");
  };

  return (
    <header className="top-bar">
      <h1 className="top-bar-title">Dashboard</h1>
      <div className="top-bar-user">
        <span className="user-name">Welcome, {userName}</span>
        <img className="user-profile" src={profilePicture} alt="Profile" />
        <button className="logout-button" onClick={handleLogout}>Logout</button>
      </div>
    </header>
  );
};

export default TopBar;
