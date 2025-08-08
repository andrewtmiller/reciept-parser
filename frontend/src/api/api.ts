// src/api/api.ts
import axios from "axios";

const api = axios.create({
  baseURL: "/api", // Assumes Vite proxy is set up
});

export default api;
