import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api"; // Centralized Axios instance
import "./TopBar.css";
import { FaUser } from "react-icons/fa";

const TopBar = () => {
  const [userName, setUserName] = useState("User");
  const [profilePicture, setProfilePicture] = useState("/profilepic.png");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await api.validateToken(localStorage.getItem("token")); // Correct function call here
        setUserName(response.data.name || "User");
        setProfilePicture(response.data.profilePic || "/profilepic.png");
        localStorage.setItem("name", response.data.name);
        localStorage.setItem("profilePic", response.data.profilePic || "/profilepic.png");
      } catch (err) {
        console.error("Token validation failed", err);
        localStorage.removeItem("token");
        navigate("/login"); // Redirect to login if token is invalid
      }
    };    

    fetchUserData();
  }, [navigate]);

  const handleLogout = () => {
    // Remove all authentication data on logout
    localStorage.removeItem("token");
    localStorage.removeItem("name");
    localStorage.removeItem("profilePic");
    navigate("/login"); // Redirect to login page
  };

  return (
    <header className="top-bar">
      <h1 className="top-bar-title">Dashboard</h1>
      <div className="top-bar-user">
        <span className="user-name">Welcome, {userName}</span>
        <img className="user-profile" src={profilePicture} alt="Profile" />
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </header>
  );
};

export default TopBar;
