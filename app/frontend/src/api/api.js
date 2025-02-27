import axios from "axios";

// Base API URL (Change this to match Flask backend)
const API_URL = "http://localhost:5000/api";

// Create Axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login if unauthorized
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
