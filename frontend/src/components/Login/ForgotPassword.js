import React from "react";
import "./Auth.css";

const ForgotPassword = () => {
  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2 className="auth-title">Reset Your Password</h2>
        <p className="auth-subtitle">Enter your email to receive a reset link.</p>
        <form className="auth-form">
          <input type="email" placeholder="Your Email" className="auth-input" />
          <button type="submit" className="auth-button">Send Reset Link</button>
        </form>
        <p className="auth-footer">
          <a href="/login" className="auth-link">Back to Login</a>
        </p>
      </div>
    </div>
  );
};

export default ForgotPassword;
