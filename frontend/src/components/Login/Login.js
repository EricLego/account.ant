import React from "react";
import "./Auth.css";

const Login = () => {
  return (
    <div className="auth-container">
      <div className="auth-card">
      <img className="auth-logo" src="/accountantlogo.png" alt="Logo"/>
        <p className="auth-subtitle">Welcome back! Log in to continue.</p>
        <form className="auth-form">
          <input type="email" placeholder="Your Email" className="auth-input" />
          <input type="password" placeholder="Your Password" className="auth-input" />
          <button type="submit" className="auth-button">Login</button>
        </form>
        <p className="auth-footer">
          Don't have an account? <a href="/signup" className="auth-link">Sign Up</a>
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
