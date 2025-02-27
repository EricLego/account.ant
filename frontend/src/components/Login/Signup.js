import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Auth.css";

const Signup = () => {
  const [firstName, setFirstName]     = useState("");
  const [lastName, setLastName]       = useState("");
  const [address, setAddress]         = useState("");
  const [dob, setDob]                 = useState("");
  const [email, setEmail]             = useState("");
  const [password, setPassword]       = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [fieldErrors, setFieldErrors] = useState({});
  const [error, setError]             = useState("");
  const [message, setMessage]         = useState("");
  
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    setFieldErrors({});

    // validate non-empty fields
    let errors = {};
    if (!firstName.trim()) errors.firstName = "First Name is required";
    if (!lastName.trim())  errors.lastName  = "Last Name is required";
    if (!address.trim())   errors.address   = "Address is required";
    if (!dob)              errors.dob       = "Date of Birth is required";
    if (!email.trim())     errors.email     = "Email is required";
    if (!password)         errors.password  = "Password is required";
    if (!confirmPassword)  errors.confirmPassword = "Please confirm your password";

    // validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email && !emailRegex.test(email)) {
      errors.email = "Please enter a valid email address";
    }
    
    // validate address
    if (address && !/\d/.test(address)) {
      errors.address = "Please enter a valid address (must include a street number)";
    }
    
    // validate pass req.
    const passwordRegex = /^[A-Za-z](?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&]).{7,}$/;
    if (password && !passwordRegex.test(password)) {
      errors.password = "Password must be at least 8 characters, start with a letter, and include a letter, a number, and a special character.";
    }
    
    // validate confirmPassword == password.
    if (password && confirmPassword && password !== confirmPassword) {
      errors.confirmPassword = "Passwords do not match";
    }
    
    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      return;
    }
    
    try {
      const response = await axios.post("http://localhost:5000/auth/signup-request", {
        firstName,
        lastName,
        address,
        dob,
        email,
        password,
      });
      setMessage("Signup request submitted! An email has been sent to the administrator for approval.");
    } catch (err) {
      console.error(err);
      setError("Failed to submit signup request. Please try again.");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <img className="auth-logo" src="/accountantlogo.png" alt="Logo" />
        <p className="auth-subtitle">Request Access to the System</p>
        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}
        <form className="auth-form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="First Name"
            className={`auth-input ${fieldErrors.firstName ? 'incomplete' : ''}`}
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
          />
          {fieldErrors.firstName && <p className="field-error">{fieldErrors.firstName}</p>}
          
          <input
            type="text"
            placeholder="Last Name"
            className={`auth-input ${fieldErrors.lastName ? 'incomplete' : ''}`}
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
          />
          {fieldErrors.lastName && <p className="field-error">{fieldErrors.lastName}</p>}
          
          <input
            type="text"
            placeholder="Address"
            className={`auth-input ${fieldErrors.address ? 'incomplete' : ''}`}
            value={address}
            onChange={(e) => setAddress(e.target.value)}
          />
          {fieldErrors.address && <p className="field-error">{fieldErrors.address}</p>}
          
          <input
            type="date"
            placeholder="Date of Birth"
            className={`auth-input ${fieldErrors.dob ? 'incomplete' : ''}`}
            value={dob}
            onChange={(e) => setDob(e.target.value)}
          />
          {fieldErrors.dob && <p className="field-error">{fieldErrors.dob}</p>}
          
          <input
            type="email"
            placeholder="Your Email"
            className={`auth-input ${fieldErrors.email ? 'incomplete' : ''}`}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          {fieldErrors.email && <p className="field-error">{fieldErrors.email}</p>}
          
          <input
            type="password"
            placeholder="Your Password"
            className={`auth-input ${fieldErrors.password ? 'incomplete' : ''}`}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {fieldErrors.password && <p className="field-error">{fieldErrors.password}</p>}
          
          <input
            type="password"
            placeholder="Confirm Password"
            className={`auth-input ${fieldErrors.confirmPassword ? 'incomplete' : ''}`}
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          {fieldErrors.confirmPassword && <p className="field-error">{fieldErrors.confirmPassword}</p>}
          
          <button type="submit" className="auth-button">Submit Request</button>
        </form>
        <p className="auth-footer">
          Already have an account? <a href="/login" className="auth-link">Login</a>
        </p>
      </div>
    </div>
  );
};

export default Signup;
