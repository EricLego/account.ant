// src/components/Login/ForgotPassword.js
import React, { useState } from "react";
import api from "../../api/api"; // Use the centralized API module
import "./Auth.css";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      await api.forgotPassword({ email });
      setMessage("Reset link sent! Check your email.");
    } catch (err) {
      console.error(err);
      setError("Failed to send reset link. Please try again.");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2 className="auth-title">Reset Your Password</h2>
        <p className="auth-subtitle">Enter your email to receive a reset link.</p>
        <form className="auth-form" onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Your Email"
            className="auth-input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button type="submit" className="auth-button">
            Send Reset Link
          </button>
        </form>
        <p className="auth-footer">
          <a href="/login" className="auth-link">
            Back to Login
          </a>
        </p>
      </div>
    </div>
  );
};

export default ForgotPassword;
