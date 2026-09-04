import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdminAuth } from '../store/useAdminAuth';
import toast from 'react-hot-toast';

export default function AdminLogin() {
  const [formData, setFormData] = useState({ admin_id: '', password: '' });
  const { login } = useAdminAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(formData);
      toast.success('Admin logged in successfully!');
      navigate('/admin/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Admin login failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 px-4">
      <div className="bg-gray-800 p-8 rounded-xl shadow-2xl w-full max-w-md border border-gray-700">
        <h2 className="text-2xl font-bold text-white mb-6 text-center">EduMind Admin Panel</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Admin ID</label>
            <input
              type="text"
              className="w-full p-2 border border-gray-600 rounded bg-gray-700 text-white"
              value={formData.admin_id}
              onChange={(e) => setFormData({...formData, admin_id: e.target.value})}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Password</label>
            <input
              type="password"
              className="w-full p-2 border border-gray-600 rounded bg-gray-700 text-white"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-red-600 hover:bg-red-700 text-white py-2 rounded font-medium transition-colors mt-4"
          >
            Access Control Panel
          </button>
        </form>
      </div>
    </div>
  );
}
