import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { api } from '../services/api';

export const useAuth = create(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      signup: async (data) => {
        const response = await api.post('/auth/signup', data);
        set({
          user: response.data.user,
          token: response.data.access_token,
          isAuthenticated: true,
        });
        return response.data;
      },

      login: async (credentials) => {
        const response = await api.post('/auth/login', credentials);
        set({
          user: response.data.user,
          token: response.data.access_token,
          isAuthenticated: true,
        });
        return response.data;
      },

      logout: () => {
        set({ user: null, token: null, isAuthenticated: false });
      },

      getProfile: async () => {
        const response = await api.get('/auth/profile');
        set({ user: response.data });
        return response.data;
      },

      updateProfile: async (data) => {
        const response = await api.put('/auth/profile', data);
        set({ user: response.data });
        return response.data;
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
