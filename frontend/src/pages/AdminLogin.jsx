import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAdminAuth } from '../store/useAdminAuth';
import toast from 'react-hot-toast';
import { Shield, Lock, ArrowLeft } from 'lucide-react';
import EduMindLogo from '../components/EduMindLogo';

export default function AdminLogin() {
  const [formData, setFormData] = useState({ admin_id: '', password: '' });
  const [loading, setLoading] = useState(false);
  const { login } = useAdminAuth();
  const navigate = useNavigate();

  React.useEffect(() => {
    document.title = "EduMind Admin — Portal Login";
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(formData);
      toast.success('Admin logged in successfully!');
      navigate('/admin/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Admin login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 px-4 relative">
      <div className="bg-slate-800 p-8 rounded-2xl shadow-2xl w-full max-w-md border border-slate-700">
        
        <div className="flex flex-col items-center justify-center mb-6">
          <EduMindLogo size={48} textClass="text-2xl font-bold tracking-tight text-white" />
          <div className="mt-2 flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-red-500/10 border border-red-500/20 text-red-400 text-[11px] font-semibold uppercase tracking-wider">
            <Shield size={12} />
            <span>Restricted Admin Portal</span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1 uppercase tracking-wider">
              Admin ID
            </label>
            <input
              type="text"
              placeholder="e.g. admin or ADMIN"
              className="w-full p-2.5 border border-slate-600 rounded-lg bg-slate-700/60 text-white placeholder-slate-400 focus:outline-none focus:border-red-500 transition-colors text-sm"
              value={formData.admin_id}
              onChange={(e) => setFormData({...formData, admin_id: e.target.value})}
              required
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1 uppercase tracking-wider">
              Password
            </label>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full p-2.5 border border-slate-600 rounded-lg bg-slate-700/60 text-white placeholder-slate-400 focus:outline-none focus:border-red-500 transition-colors text-sm"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-red-600 hover:bg-red-500 text-white py-2.5 rounded-lg font-semibold transition-all shadow-lg text-sm flex items-center justify-center gap-2 mt-4 disabled:opacity-50"
          >
            <Lock size={16} />
            <span>{loading ? 'Authenticating...' : 'Access Control Panel'}</span>
          </button>
        </form>

        <div className="mt-6 pt-4 border-t border-slate-700/60 flex items-center justify-center">
          <Link to="/login" className="text-xs text-slate-400 hover:text-slate-200 flex items-center gap-1 transition-colors">
            <ArrowLeft size={14} />
            <span>Return to Student Login</span>
          </Link>
        </div>

      </div>
    </div>
  );
}
