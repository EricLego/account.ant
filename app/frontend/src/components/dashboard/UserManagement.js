// src/components/dashboard/UserManagement.js
import React, { useState } from "react";
import DashboardNav from "./DashboardNav";
import TopBar from "./TopBar";
import "./UserManagement.css";

const UserManagement = () => {
  // hardcoded data
  const initialUsers = [
    {
      id: 1,
      firstName: "Alice",
      lastName: "Smith",
      email: "alice@example.com",
      role: "Regular User",
      active: true,
    },
    {
      id: 2,
      firstName: "Bob",
      lastName: "Jones",
      email: "bob@example.com",
      role: "Manager",
      active: true,
    },
    {
      id: 3,
      firstName: "Charlie",
      lastName: "Brown",
      email: "charlie@example.com",
      role: "Regular User",
      active: false,
    },
  ];
  const [users, setUsers] = useState(initialUsers);
  const [newUser, setNewUser] = useState({
    firstName: "",
    lastName: "",
    email: "",
    role: "Regular User",
  });
  const [editingUser, setEditingUser] = useState(null);
  const [editUserData, setEditUserData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    role: "",
    active: true,
  });

  const handleNewUserChange = (e) => {
    setNewUser({ ...newUser, [e.target.name]: e.target.value });
  };

  const handleAddUser = (e) => {
    e.preventDefault();
    const id = users.length ? Math.max(...users.map((u) => u.id)) + 1 : 1;
    const userToAdd = { id, ...newUser, active: true };
    setUsers([...users, userToAdd]);
    setNewUser({
      firstName: "",
      lastName: "",
      email: "",
      role: "Regular User",
    });
  };

  const handleEditClick = (user) => {
    setEditingUser(user.id);
    setEditUserData(user);
  };

  const handleEditChange = (e) => {
    setEditUserData({ ...editUserData, [e.target.name]: e.target.value });
  };

  const handleSaveEdit = (e) => {
    e.preventDefault();
    setUsers(users.map((u) => (u.id === editingUser ? editUserData : u)));
    setEditingUser(null);
  };

  const toggleUserActive = (id) => {
    setUsers(
      users.map((u) =>
        u.id === id ? { ...u, active: !u.active } : u
      )
    );
  };

  return (
    <div className="home-layout">
      <DashboardNav />
      <div className="home-main">
        <TopBar title="User Management" />
        <div className="home-content">
          {/* create new user */}
          <div className="create-user-form">
            <h3>Create New User</h3>
            <form onSubmit={handleAddUser}>
              <input
                type="text"
                name="firstName"
                placeholder="First Name"
                value={newUser.firstName}
                onChange={handleNewUserChange}
              />
              <input
                type="text"
                name="lastName"
                placeholder="Last Name"
                value={newUser.lastName}
                onChange={handleNewUserChange}
              />
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={newUser.email}
                onChange={handleNewUserChange}
              />
              <select
                name="role"
                value={newUser.role}
                onChange={handleNewUserChange}
              >
                <option value="Administrator">Administrator</option>
                <option value="Manager">Manager</option>
                <option value="Regular User">Regular User</option>
              </select>
              <button type="submit">Add User</button>
            </form>
          </div>

          {/* existing users */}
          <div className="user-list">
            <h3>Existing Users</h3>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td>
                      {editingUser === user.id ? (
                        <input
                          type="text"
                          name="firstName"
                          value={editUserData.firstName}
                          onChange={handleEditChange}
                        />
                      ) : (
                        `${user.firstName} ${user.lastName}`
                      )}
                    </td>
                    <td>
                      {editingUser === user.id ? (
                        <input
                          type="email"
                          name="email"
                          value={editUserData.email}
                          onChange={handleEditChange}
                        />
                      ) : (
                        user.email
                      )}
                    </td>
                    <td>
                      {editingUser === user.id ? (
                        <select
                          name="role"
                          value={editUserData.role}
                          onChange={handleEditChange}
                        >
                          <option value="Administrator">Administrator</option>
                          <option value="Manager">Manager</option>
                          <option value="Regular User">Regular User</option>
                        </select>
                      ) : (
                        user.role
                      )}
                    </td>
                    <td>{user.active ? "Active" : "Inactive"}</td>
                    <td>
                      {editingUser === user.id ? (
                        <button onClick={handleSaveEdit}>Save</button>
                      ) : (
                        <>
                          <button onClick={() => handleEditClick(user)}>Edit</button>
                          <button onClick={() => toggleUserActive(user.id)}>
                            {user.active ? "Deactivate" : "Activate"}
                          </button>
                        </>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserManagement;
