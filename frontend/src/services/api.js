import axios from 'axios';
import { useAuth } from '../store/useAuth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
});

import { useAdminAuth } from '../store/useAdminAuth';

api.interceptors.request.use((config) => {
  const isAdminRoute = config.url.startsWith('/admin');
  
  if (isAdminRoute) {
    const adminToken = useAdminAuth.getState().token;
    if (adminToken) {
      config.headers.Authorization = `Bearer ${adminToken}`;
    }
  } else {
    const userToken = useAuth.getState().token;
    if (userToken) {
      config.headers.Authorization = `Bearer ${userToken}`;
    }
  }
  return config;
});
