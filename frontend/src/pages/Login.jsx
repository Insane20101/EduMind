import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../store/useAuth';
import toast from 'react-hot-toast';
import axios from 'axios';
import { KeyRound, X, Loader2, Send, ShieldCheck, RefreshCw, Lock, Mail } from 'lucide-react';
import EduMindLogo from '../components/EduMindLogo';

import { getApiBaseUrl } from '../config';

export default function Login() {
  const [formData, setFormData] = useState({ enrollment: '', password: '' });
  
  // Forgot Password Recovery State
  const [showResetModal, setShowResetModal] = useState(false);
  const [resetStep, setResetStep] = useState(1); // 1: Enrollment + Recovery Email ➔ Send OTP, 2: OTP + New Password
  const [resetEnrollment, setResetEnrollment] = useState('');
  const [recoveryEmail, setRecoveryEmail] = useState('');
  const [otpCode, setOtpCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [maskedEmail, setMaskedEmail] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    document.title = "EduMind — Student Login";
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(formData);
      toast.success('Logged in successfully!');
      navigate('/');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Login failed');
    }
  };

  // Step 1: Verify Enrollment + Recovery Email & Send Resend OTP
  const handleSendOTP = async (e) => {
    e.preventDefault();
    if (!resetEnrollment.trim()) {
      toast.error('Please enter your Enrollment Number.');
      return;
    }
    if (!recoveryEmail.trim()) {
      toast.error('Please enter your registered Recovery Email ID.');
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post(`${getApiBaseUrl()}/api/auth/send-otp`, {
        enrollment: resetEnrollment.trim().toUpperCase(),
        recovery_email: recoveryEmail.trim().toLowerCase()
      });
      
      setMaskedEmail(res.data.masked_email || recoveryEmail);
      toast.success(res.data.message || 'Verification code sent to your Recovery Email!');
      setResetStep(2);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to send verification code. Please check your inputs.');
    } finally {
      setLoading(false);
    }
  };

  // Step 2: Verify 6-digit OTP code & Reset Password
  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    if (!otpCode.trim() || otpCode.trim().length !== 6) {
      toast.error('Please enter the 6-digit code sent to your Recovery Email.');
      return;
    }
    if (!newPassword.trim() || newPassword.length < 8) {
      toast.error('New password must be at least 8 characters long.');
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post(`${getApiBaseUrl()}/api/auth/verify-otp-reset-password`, {
        enrollment: resetEnrollment.trim().toUpperCase(),
        otp_code: otpCode.trim(),
        new_password: newPassword.trim()
      });

      toast.success(res.data?.message || 'Password reset successfully!');
      // Pre-fill login credentials with Enrollment + New Password
      setFormData({
        enrollment: resetEnrollment.trim().toUpperCase(),
        password: newPassword.trim()
      });
      // Close modal and reset state
      setShowResetModal(false);
      setResetStep(1);
      setOtpCode('');
      setNewPassword('');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Verification failed. Please check the 6-digit code.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-app px-4 relative">
      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md border border-border-subtle">
        <div className="flex flex-col items-center mb-6">
          <EduMindLogo size={44} textClass="text-2xl font-bold tracking-tight text-slate-900" />
          <p className="text-xs text-text-secondary mt-1">Student Academic Gateway</p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-text-primary mb-1">Enrollment Number</label>
            <input
              type="text"
              placeholder="e.g. 2023CSD0517"
              className="w-full p-2.5 border border-border-subtle rounded-lg bg-muted text-text-primary focus:outline-none focus:border-primary transition-colors text-sm uppercase"
              value={formData.enrollment}
              onChange={(e) => setFormData({...formData, enrollment: e.target.value.toUpperCase()})}
              required
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-sm font-medium text-text-primary">Password</label>
              <button
                type="button"
                onClick={() => {
                  setResetEnrollment(formData.enrollment);
                  setResetStep(1);
                  setShowResetModal(true);
                }}
                className="text-xs font-semibold text-accent hover:underline flex items-center gap-1"
              >
                <KeyRound size={12} />
                <span>Forgot password?</span>
              </button>
            </div>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full p-2.5 border border-border-subtle rounded-lg bg-muted text-text-primary focus:outline-none focus:border-primary transition-colors text-sm"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-primary hover:bg-primary-hover text-white py-2.5 rounded-lg font-medium transition-colors shadow-sm text-sm"
          >
            Log In
          </button>
        </form>

        <p className="mt-5 text-center text-sm text-text-secondary">
          Don't have an account? <Link to="/signup" className="text-accent hover:underline font-semibold">Sign up</Link>
        </p>

        <p className="mt-3 pt-3 border-t border-border-subtle text-center text-xs text-text-secondary">
          Are you an Administrator? <Link to="/admin/login" className="text-primary hover:underline font-bold">Admin Portal</Link>
        </p>
      </div>

      {/* Modern 2-Factor Recovery Password Reset Modal */}
      {showResetModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4 animate-in fade-in duration-200">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl border border-slate-200 relative animate-in zoom-in-95 duration-150">
            
            <button
              onClick={() => {
                setShowResetModal(false);
                setResetStep(1);
              }}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-700 p-1 rounded-lg transition-colors"
            >
              <X size={18} />
            </button>

            <div className="flex items-center gap-2 text-primary font-bold text-lg mb-1">
              <ShieldCheck size={22} className="text-accent" />
              <span>Password Recovery</span>
            </div>
            <p className="text-xs text-slate-500 mb-5 leading-relaxed">
              {resetStep === 1 
                ? 'Enter your Enrollment Number and your registered Recovery Email ID to receive a 6-digit OTP code.' 
                : `Enter the 6-digit OTP code sent to ${maskedEmail} and create your new password.`}
            </p>

            {/* STEP 1: Verify Enrollment + Recovery Email */}
            {resetStep === 1 && (
              <form onSubmit={handleSendOTP} className="space-y-3.5">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1 uppercase tracking-wider">
                    Enrollment Number
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. 2023CSD0517"
                    className="w-full p-2.5 border border-slate-300 rounded-lg text-xs bg-slate-50 text-slate-900 focus:bg-white focus:border-primary outline-none transition-all uppercase"
                    value={resetEnrollment}
                    onChange={(e) => setResetEnrollment(e.target.value.toUpperCase())}
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1 uppercase tracking-wider flex items-center gap-1">
                    <Mail size={12} className="text-accent" />
                    <span>Registered Recovery Email ID</span>
                  </label>
                  <input
                    type="email"
                    placeholder="e.g. student@gmail.com"
                    className="w-full p-2.5 border border-slate-300 rounded-lg text-xs bg-slate-50 text-slate-900 focus:bg-white focus:border-primary outline-none transition-all"
                    value={recoveryEmail}
                    onChange={(e) => setRecoveryEmail(e.target.value)}
                    required
                  />
                </div>

                <div className="pt-2 flex items-center justify-end gap-2">
                  <button
                    type="button"
                    onClick={() => setShowResetModal(false)}
                    className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
                  >
                    Cancel
                  </button>

                  <button
                    type="submit"
                    disabled={loading}
                    className="px-4 py-2 text-xs font-semibold bg-primary hover:bg-primary-hover text-white rounded-lg transition-all shadow-md flex items-center gap-1.5 disabled:opacity-50"
                  >
                    {loading ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
                    <span>Send 6-Digit OTP</span>
                  </button>
                </div>
              </form>
            )}

            {/* STEP 2: Verify 6-Digit OTP & Create New Password */}
            {resetStep === 2 && (
              <form onSubmit={handleVerifyOTP} className="space-y-3.5">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1 uppercase tracking-wider">
                    6-Digit Verification OTP Code
                  </label>
                  <input
                    type="text"
                    maxLength={6}
                    placeholder="123456"
                    className="w-full p-3 border border-slate-300 rounded-lg text-center font-mono text-lg font-bold tracking-widest text-primary bg-slate-50 focus:bg-white focus:border-primary outline-none transition-all"
                    value={otpCode}
                    onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, ''))}
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1 uppercase tracking-wider">
                    New Password (min 8 chars)
                  </label>
                  <input
                    type="password"
                    placeholder="••••••••"
                    className="w-full p-2.5 border border-slate-300 rounded-lg text-xs bg-slate-50 text-slate-900 focus:bg-white focus:border-primary outline-none transition-all"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                  />
                </div>

                <div className="flex items-center justify-between pt-2">
                  <button
                    type="button"
                    onClick={handleSendOTP}
                    disabled={loading}
                    className="text-xs text-accent hover:underline flex items-center gap-1 font-medium"
                  >
                    <RefreshCw size={12} />
                    <span>Resend Code</span>
                  </button>

                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => setResetStep(1)}
                      className="px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
                    >
                      Back
                    </button>

                    <button
                      type="submit"
                      disabled={loading || otpCode.length !== 6}
                      className="px-4 py-2 text-xs font-semibold bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg transition-all shadow-md flex items-center gap-1.5 disabled:opacity-50"
                    >
                      {loading ? <Loader2 size={14} className="animate-spin" /> : <Lock size={14} />}
                      <span>Reset Password</span>
                    </button>
                  </div>
                </div>
              </form>
            )}

          </div>
        </div>
      )}
    </div>
  );
}
