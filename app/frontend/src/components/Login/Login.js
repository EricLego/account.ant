// src/components/Login/Login.js
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../../api/api"; // Ensure this function uses relative URLs internally
import "./Auth.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/home"); // Updated from "/dashboard" to "/home"
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
  
    try {
      const response = await login({ email, password });
      localStorage.setItem("token", response.data.token);
      localStorage.setItem("role", response.data.role);
  
      // Save user details
      const user = { 
        username: "John Doe", // Or fetch the user details from the response if available
        profilePic: "/profile-pic.jpg" // Mock profile pic
      };
      localStorage.setItem("user", JSON.stringify(user));
  
      navigate("/home"); // Redirect to home/dashboard
    } catch (err) {
      console.error("Login failed", err);
  
      if (err.response) {
        if (err.response.status === 401) {
          setError("Invalid email or password. Please try again.");
        } else {
          setError("Server error. Please try again later.");
        }
      } else {
        console.warn("Bypassing network error for testing purposes.");
        localStorage.setItem("token", "mock-token");
        localStorage.setItem("role", "regular"); // or any role you prefer
        navigate("/home");
      }
    }
  };  

  return (
    <div className="auth-container">
      <div className="auth-card">
        <img className="auth-logo" src="/accountantlogo.png" alt="Logo" />
        <p className="auth-subtitle">Welcome back! Log in to continue.</p>

        {error && <p className="auth-error">{error}</p>}

        <form className="auth-form" onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Your Email"
            className="auth-input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Your Password"
            className="auth-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" className="auth-button">Login</button>
        </form>

        <p className="auth-footer">
          Don't have an account? <a href="/signup" className="auth-link">Request Access</a>
        </p>
        
        <div className="auth-divider">
          <span>or</span>
        </div>

        <p className="auth-footer">
          <a href="/forgot-password" className="auth-goto-forgot">Reset Password</a>
        </p>
      </div>
    </div>
  );
};

export default Login;
