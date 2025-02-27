import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login/Login";
import Signup from "./components/Login/Signup";
import ForgotPassword from "./components/Login/ForgotPassword";

import Dashboard from "./components/dashboard/Dashboard";

import ResetPassword from "./components/Login/ResetPassword"
import Home from "./components/dashboard/Home"


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/dashboard" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;
