import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Auth.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  
  const navigate = useNavigate();

  // hardcoded testing
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (email === "regular@accountant.com" && password === "colony") {
      const token = "dummy-token-regular";
      localStorage.setItem("token", token);
      localStorage.setItem("role", "Regular User");
      alert("Login successful");
      navigate("/dashboard");
    } else if (email === "manager@accountant.com" && password === "colony") {
      const token = "dummy-token-manager";
      localStorage.setItem("token", token);
      localStorage.setItem("role", "Manager");
      alert("Login successful");
      navigate("/dashboard");
    } else if (email === "admin@accountant.com" && password === "colony") {
      const token = "dummy-token-admin";
      localStorage.setItem("token", token);
      localStorage.setItem("role", "Administrator");
      alert("Login successful");
      navigate("/dashboard");
    } else {
      setError("Invalid credentials. Please try again.");
    }
  };


  // commeting this section out for now until API updated
  /*
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post("http://localhost:5000/auth/login", {
        email, 
        password
      });
      const token = response.data.token;
      localStorage.setItem("token", token);
      alert("Login successful");
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError("Invalid credentials. Please try again.");
    }
  };
  */

  return (
    <div className="auth-container">
      <div className="auth-card">
      <img className="auth-logo" src="/accountantlogo.png" alt="Logo"/>
        <p className="auth-subtitle">Welcome back! Log in to continue.</p>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <form className="auth-form" onSubmit={handleSubmit}>
          <input
              type="email"
              placeholder="Your Email"
              className="auth-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type="password"
              placeholder="Your Password"
              className="auth-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
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
