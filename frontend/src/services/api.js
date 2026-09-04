import axios from 'axios';
import { useAuth } from '../store/useAuth';
import { useAdminAuth } from '../store/useAdminAuth';
import { getApiUrl } from '../config';

export const api = axios.create();

api.interceptors.request.use((config) => {
  // Dynamically attach baseURL so runtime hostname changes are reflected
  config.baseURL = getApiUrl();

  const isAdminRoute = config.url && config.url.startsWith('/admin');
  
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
