import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { api } from '../services/api';

export const useAdminAuth = create(
  persist(
    (set) => ({
      token: null,
      isAuthenticated: false,

      login: async (credentials) => {
        const response = await api.post('/admin/auth/login', credentials);
        set({
          token: response.data.access_token,
          isAuthenticated: true,
        });
        return response.data;
      },

      logout: () => {
        set({ token: null, isAuthenticated: false });
      },

      updateCredentials: async (data) => {
        const response = await api.put('/admin/auth/credentials', data);
        if (response.data.access_token) {
           set({ token: response.data.access_token });
        }
        return response.data;
      },
    }),
    {
      name: 'admin-auth-storage',
    }
  )
);
