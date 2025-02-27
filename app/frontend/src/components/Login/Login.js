import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api"; // Use centralized Axios instance
import "./Auth.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Redirect if already logged in
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/dashboard");
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); // Reset error message on new attempt

    try {
      const response = await api.post("/auth/login", { email, password });

      // Store token & role in localStorage
      localStorage.setItem("token", response.data.token);
      localStorage.setItem("role", response.data.role);

      // Redirect to dashboard
      navigate("/dashboard");
    } catch (err) {
      console.error("Login failed", err);

      // Handle different error cases
      if (err.response) {
        if (err.response.status === 401) {
          setError("Invalid email or password. Please try again.");
        } else {
          setError("Server error. Please try again later.");
        }
      } else {
        setError("Network error. Check your connection.");
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
