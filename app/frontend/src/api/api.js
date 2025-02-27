// src/api/api.js
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000'; // Adjust if needed

export const signupRequest = (userData) => {
  return axios.post(`${API_BASE_URL}/auth/signup-request`, userData);
};

export const approveUser = (approvalData) => {
  return axios.post(`${API_BASE_URL}/admin/approve_user`, approvalData);
};

export const login = (credentials) => {
  return axios.post(`${API_BASE_URL}/auth/login`, credentials);
};

export const forgotPassword = (data) => {
  return axios.post(`${API_BASE_URL}/auth/forgot-password`, data);
};

export const updatePassword = (data) => {
  return axios.post(`${API_BASE_URL}/auth/update-password`, data);
};

export const updateUser = (userData) => {
  return axios.post(`${API_BASE_URL}/admin/update_user`, userData);
};

export const suspendUser = (data) => {
  return axios.post(`${API_BASE_URL}/admin/suspend_user`, data);
};

export const viewUsers = () => {
  return axios.get(`${API_BASE_URL}/admin/view_users`);
};

export const reportExpiredPasswords = () => {
  return axios.get(`${API_BASE_URL}/admin/report_expired_passwords`);
};

export const sendEmail = (data) => {
  return axios.post(`${API_BASE_URL}/admin/send_email`, data);
};

// Default export so you can import it as 'api'
export default {
  signupRequest,
  approveUser,
  login,
  forgotPassword,
  updatePassword,
  updateUser,
  suspendUser,
  viewUsers,
  reportExpiredPasswords,
  sendEmail,
};
