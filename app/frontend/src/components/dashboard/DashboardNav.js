// src/components/dashboard/DashboardNav.js
import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./DashboardNav.css";

import { FaHome } from "react-icons/fa";
import { BiSolidReport } from "react-icons/bi";
import { FaUsersCog } from "react-icons/fa";
import { FaUser } from "react-icons/fa";
import { RiLockPasswordFill } from "react-icons/ri";

const DashboardNav = () => {
  const navigate = useNavigate();
  const role = localStorage.getItem("role") || "Regular User";

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("name");
    navigate("/login");
  };

  return (
    <aside className="dashboard-nav">
      <div className="nav-brand">
        <img className="brand-logo" src="/accountantlogo.png" alt="Logo" />
      </div>

      <nav className="nav-links">
        <ul>
          <li>
            <Link to="/home" className="nav-item">
              <span className="nav-icon">
                <FaHome />
              </span>
              <span>Dashboard</span>
            </Link>
          </li>

          {role === "Administrator" && (
            <>
              <li>
                <Link to="/user-management" className="nav-item">
                  <span className="nav-icon">
                    <FaUsersCog />
                  </span>
                  <span>User Management</span>
                </Link>
              </li>
              <li>
                <Link to="/admin-reports" className="nav-item">
                  <span className="nav-icon">
                    <BiSolidReport />
                  </span>
                  <span>Admin Reports</span>
                </Link>
              </li>
            </>
          )}

          <li>
            <Link to="/profile" className="nav-item">
              <span className="nav-icon">
                <FaUser />
              </span>
              <span>Profile</span>
            </Link>
          </li>
          <li>
            <Link to="/reset-password" className="nav-item">
              <span className="nav-icon">
                <RiLockPasswordFill />
              </span>
              <span>Change Password</span>
            </Link>
          </li>
        </ul>
      </nav>

      <div className="nav-footer">
        <button onClick={handleLogout} className="logout-btn">
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
};

export default DashboardNav;
