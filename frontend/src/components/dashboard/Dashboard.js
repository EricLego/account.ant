import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css"; // Make sure this file exists in the same directory

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is stored in localStorage
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    } else {
      navigate("/login"); // Redirect to login if no user is found
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("user"); // Remove user from localStorage
    navigate("/login"); // Redirect to login page
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-topbar">
        <div className="dashboard-logo">MyApp</div>
        <nav className="dashboard-nav">
          <a href="/home">Home</a>
          <a href="/profile">Profile</a>
          <a href="/settings">Settings</a>
        </nav>
        {user && (
          <div className="dashboard-user">
            <img src={user.profilePic} alt="Profile" className="dashboard-avatar" />
            <span className="dashboard-username">{user.username}</span>
            <button className="dashboard-logout" onClick={handleLogout}>
              Logout
            </button>
          </div>
        )}
      </header>
      <main className="dashboard-content">
        <h1>Welcome, {user ? user.username : "Guest"}!</h1>
        <p>Dashboard is under construction 🚧</p>
      </main>
    </div>
  );
};

export default Dashboard;
