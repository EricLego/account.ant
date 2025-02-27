import React, { useState } from "react";
import DashboardNav from "./DashboardNav";
import TopBar from "./TopBar";
import "./AdminReports.css";

const AdminReports = () => {
  // hardcoded data
  const initialUsers = [
    {
      id: 1,
      firstName: "Alice",
      lastName: "Smith",
      email: "alice@example.com",
      role: "Regular User",
      active: true,
      passwordExpiry: "2023-01-01",
      suspended: false,
    },
    {
      id: 2,
      firstName: "Bob",
      lastName: "Jones",
      email: "bob@example.com",
      role: "Manager",
      active: true,
      passwordExpiry: "2024-05-01",
      suspended: false,
    },
    {
      id: 3,
      firstName: "Charlie",
      lastName: "Brown",
      email: "charlie@example.com",
      role: "Regular User",
      active: false,
      passwordExpiry: "2022-12-01",
      suspended: false,
    },
  ];
  const [users, setUsers] = useState(initialUsers);
  const [suspensionInfo, setSuspensionInfo] = useState({
    userId: "",
    startDate: "",
    endDate: "",
  });
  const [emailInfo, setEmailInfo] = useState({
    userId: "",
    subject: "",
    message: "",
  });
  const [emailStatus, setEmailStatus] = useState("");

  const handleSuspend = (e) => {
    e.preventDefault();
    const { userId, startDate, endDate } = suspensionInfo;
    if (!userId || !startDate || !endDate) {
      alert("Please fill in all fields for suspension.");
      return;
    }
    setUsers(
      users.map((user) =>
        user.id === parseInt(userId)
          ? { ...user, suspended: true, suspensionStart: startDate, suspensionEnd: endDate }
          : user
      )
    );
    setSuspensionInfo({ userId: "", startDate: "", endDate: "" });
    alert("User suspended successfully.");
  };

  const handleSendEmail = (e) => {
    e.preventDefault();
    // waiting for backend logic to create API call for email sends
    setEmailStatus("Email sent successfully.");
    setEmailInfo({ userId: "", subject: "", message: "" });
  };

  const today = new Date().toISOString().split("T")[0];
  const expiredPasswords = users.filter((user) => user.passwordExpiry < today);

  return (
    <div className="home-layout">
      <DashboardNav />
      <div className="home-main">
      <TopBar title="Admin Reports" />
        <div className="home-content">

          {/* user report */}
          <section className="report-section">
            <h3>All Users</h3>
            <div className="user-report">
              {users.map((user) => (
                <div key={user.id} className="user-card">
                  <p className="user-name">
                    {user.firstName} {user.lastName}
                  </p>
                  <p className="user-email">{user.email}</p>
                  <p className="user-role">Role: {user.role}</p>
                  <p className="user-status">
                    Active: {user.active ? "Yes" : "No"} | Suspended:{" "}
                    {user.suspended ? "Yes" : "No"}
                  </p>
                </div>
              ))}
            </div>
          </section>

          {/* suspend user */}
          <section className="report-section">
            <h3>Suspend User (Extended Leave)</h3>
            <form onSubmit={handleSuspend} className="suspend-form">
              <select
                value={suspensionInfo.userId}
                onChange={(e) =>
                  setSuspensionInfo({ ...suspensionInfo, userId: e.target.value })
                }
              >
                <option value="">Select User</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.firstName} {user.lastName} ({user.email})
                  </option>
                ))}
              </select>
              <input
                type="date"
                value={suspensionInfo.startDate}
                onChange={(e) =>
                  setSuspensionInfo({ ...suspensionInfo, startDate: e.target.value })
                }
                placeholder="Start Date"
              />
              <input
                type="date"
                value={suspensionInfo.endDate}
                onChange={(e) =>
                  setSuspensionInfo({ ...suspensionInfo, endDate: e.target.value })
                }
                placeholder="End Date"
              />
              <button type="submit">Suspend User</button>
            </form>
          </section>

          {/* expired password reports */}
          <section className="report-section">
            <h3>Expired Passwords</h3>
            {expiredPasswords.length > 0 ? (
              <table className="users-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Password Expiry</th>
                  </tr>
                </thead>
                <tbody>
                  {expiredPasswords.map((user) => (
                    <tr key={user.id}>
                      <td>
                        {user.firstName} {user.lastName}
                      </td>
                      <td>{user.email}</td>
                      <td>{user.passwordExpiry}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No expired passwords.</p>
            )}
          </section>

          {/* send email to users */}
          <section className="report-section">
            <h3>Send Email to User</h3>
            <form onSubmit={handleSendEmail} className="email-form">
              <select
                value={emailInfo.userId}
                onChange={(e) =>
                  setEmailInfo({ ...emailInfo, userId: e.target.value })
                }
              >
                <option value="">Select User</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.firstName} {user.lastName} ({user.email})
                  </option>
                ))}
              </select>
              <input
                type="text"
                placeholder="Subject"
                value={emailInfo.subject}
                onChange={(e) =>
                  setEmailInfo({ ...emailInfo, subject: e.target.value })
                }
              />
              <textarea
                placeholder="Message"
                value={emailInfo.message}
                onChange={(e) =>
                  setEmailInfo({ ...emailInfo, message: e.target.value })
                }
              />
              <button type="submit">Send Email</button>
              {emailStatus && <p className="email-status">{emailStatus}</p>}
            </form>
          </section>
        </div>
      </div>
    </div>
  );
};

export default AdminReports;
