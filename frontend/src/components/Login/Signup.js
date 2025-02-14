import React from "react";
import "./Auth.css";

const Signup = () => {
  return (
    <div className="auth-container">
      <div className="auth-card">
        <img className="auth-logo" src="/accountantlogo.png" alt="Logo"/>
        <p className="auth-subtitle">Join the colony today!</p>
        <form className="auth-form">
          <input type="text" placeholder="Your Name" className="auth-input" />
          <input type="email" placeholder="Your Email" className="auth-input" />
          <input type="password" placeholder="Your Password" className="auth-input" />
          <button type="submit" className="auth-button">Sign Up</button>
        </form>
        <p className="auth-footer">
          Already have an account? <a href="/login" className="auth-link">Login</a>
        </p>
      </div>
    </div>
  );
};

export default Signup;
