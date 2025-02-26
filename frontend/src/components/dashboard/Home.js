import React from "react";
import DashboardNav from "./DashboardNav"
import TopBar from "./TopBar"
import "./Home.css";

const Home = () => {
  return (
    <div className="home-layout">
      <DashboardNav />
      <div className="home-main">
        <TopBar />
        <div className="home-content">
          <p style={{ color: "#999" }}>Welcome to the Dashboard!</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
