// Authentication service for making API calls to the backend

import axios from 'axios';

const API_URL = '/api'; // Update with actual API URL

// Setting up axios defaults
axios.defaults.headers.post['Content-Type'] = 'application/json';

// Add auth token to requests if user is logged in
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Handle 401 responses (unauthorized)
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Logout user if token is invalid/expired
      logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Login user
const login = async (username, password) => {
  try {
    const response = await axios.post(`${API_URL}/auth/login`, { username, password });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Network error' };
  }
};

// Register new user
const register = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/auth/register`, userData);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Network error' };
  }
};

// Forgot password
const forgotPassword = async (email, username) => {
  try {
    const response = await axios.post(`${API_URL}/auth/forgot-password`, { email, username });
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Network error' };
  }
};

// Reset password
const resetPassword = async (oldPassword, newPassword) => {
  try {
    const response = await axios.post(`${API_URL}/auth/reset-password`, { old_password: oldPassword, new_password: newPassword });
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Network error' };
  }
};

// Logout user
const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

// Get current user from localStorage
const getCurrentUser = () => {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
};

// Check if user is authenticated
const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};

// Check if current user has required role
const hasRole = (role) => {
  const user = getCurrentUser();
  return user && user.role === role;
};

const authService = {
  login,
  register,
  forgotPassword,
  resetPassword,
  logout,
  getCurrentUser,
  isAuthenticated,
  hasRole
};

export default authService;