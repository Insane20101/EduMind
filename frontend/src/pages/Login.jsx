import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../store/useAuth';
import toast from 'react-hot-toast';

export default function Login() {
  const [formData, setFormData] = useState({ enrollment: '', password: '' });
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await login(formData);
      toast.success('Logged in successfully!');
      navigate('/');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-app px-4">
      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md border border-border-subtle">
        <h2 className="text-2xl font-bold text-primary mb-6 text-center">Login to EduMind</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-text-primary mb-1">Enrollment Number</label>
            <input
              type="text"
              placeholder="e.g. 2023CSE0123"
              className="w-full p-2 border border-border-subtle rounded bg-muted text-text-primary"
              value={formData.enrollment}
              onChange={(e) => setFormData({...formData, enrollment: e.target.value.toUpperCase()})}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-text-primary mb-1">Password</label>
            <input
              type="password"
              className="w-full p-2 border border-border-subtle rounded bg-muted text-text-primary"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-primary hover:bg-primary-hover text-white py-2 rounded font-medium transition-colors"
          >
            Log In
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-text-secondary">
          Don't have an account? <Link to="/signup" className="text-accent hover:underline">Sign up</Link>
        </p>
      </div>
    </div>
  );
}
