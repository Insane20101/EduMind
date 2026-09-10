import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../store/useAuth';
import toast from 'react-hot-toast';
import axios from 'axios';
import { Eye, EyeOff, Loader2, Mail, ShieldCheck, RefreshCw, X, ArrowLeft } from 'lucide-react';
import EduMindLogo from '../components/EduMindLogo';
import { getApiBaseUrl } from '../config';

export default function Signup() {
  const [formData, setFormData] = useState({
    enrollment: '',
    recovery_email: '',
    branch: 'CSE',
    semester: 'Semester-3',
    first_name: '',
    middle_name: '',
    last_name: '',
    password: '',
    confirm_password: ''
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // 2-Step OTP Modal & Verification State
  const [showOtpModal, setShowOtpModal] = useState(false);
  const [otpCode, setOtpCode] = useState('');
  const [maskedEmail, setMaskedEmail] = useState('');
  const [sendingOtp, setSendingOtp] = useState(false);
  const [verifying, setVerifying] = useState(false);
  const [cooldown, setCooldown] = useState(0);

  const { signup } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    document.title = "EduMind — Create Account";
  }, []);

  // Cooldown countdown timer for OTP resend
  useEffect(() => {
    let timer;
    if (cooldown > 0) {
      timer = setInterval(() => {
        setCooldown((prev) => prev - 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [cooldown]);

  const handleEnrollmentChange = (e) => {
    let val = e.target.value.toUpperCase();
    setFormData({ ...formData, enrollment: val });
  };

  const ENROLL_REGEX = /^(?=.*\d)[A-Za-z0-9\/-]{8,20}$/;

  // Step 1: Request Signup OTP
  const handleRequestOtp = async (e) => {
    e.preventDefault();
    const cleanEnr = formData.enrollment.trim().toUpperCase();
    if (!ENROLL_REGEX.test(cleanEnr)) {
      toast.error('Invalid Enrollment format. Must be 8-20 characters with digits (e.g. 2023CSD0517 or 2100970100045)');
      return;
    }
    if (formData.branch !== 'CSE') {
      toast.error(`Registration is currently only available for ${formData.branch}`);
      return;
    }
    if (formData.password !== formData.confirm_password) {
      toast.error('Passwords do not match');
      return;
    }
    if (!formData.recovery_email.trim()) {
      toast.error('Recovery Email ID is required');
      return;
    }

    setSendingOtp(true);
    try {
      const res = await axios.post(`${getApiBaseUrl()}/api/auth/send-signup-otp`, {
        enrollment: formData.enrollment.trim().toUpperCase(),
        recovery_email: formData.recovery_email.trim().toLowerCase(),
        first_name: formData.first_name.trim()
      });

      setMaskedEmail(res.data.masked_email || formData.recovery_email);
      toast.success(res.data.message || 'Verification code sent to your email!');
      setShowOtpModal(true);
      setCooldown(30); // 30 second resend cooldown
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to send verification code.');
    } finally {
      setSendingOtp(false);
    }
  };

  // Resend OTP trigger
  const handleResendOtp = async () => {
    if (cooldown > 0) return;
    setSendingOtp(true);
    try {
      const res = await axios.post(`${getApiBaseUrl()}/api/auth/send-signup-otp`, {
        enrollment: formData.enrollment.trim().toUpperCase(),
        recovery_email: formData.recovery_email.trim().toLowerCase(),
        first_name: formData.first_name.trim()
      });

      toast.success(res.data.message || 'New verification code sent!');
      setCooldown(30);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to resend verification code.');
    } finally {
      setSendingOtp(false);
    }
  };

  // Step 2: Verify OTP & Submit Registration
  const handleFinalSignup = async (e) => {
    e.preventDefault();
    if (!otpCode.trim() || otpCode.trim().length !== 6) {
      toast.error('Please enter the 6-digit code sent to your email.');
      return;
    }

    setVerifying(true);
    try {
      const { confirm_password, ...submitData } = formData;
      await signup({
        ...submitData,
        enrollment: submitData.enrollment.trim().toUpperCase(),
        recovery_email: submitData.recovery_email.trim().toLowerCase(),
        otp_code: otpCode.trim()
      });

      toast.success('Account created successfully!');
      setShowOtpModal(false);
      navigate('/');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Verification failed. Please check the code.');
    } finally {
      setVerifying(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-app px-4 py-8 relative">
      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-lg border border-border-subtle">
        <div className="flex flex-col items-center mb-6">
          <EduMindLogo size={44} textClass="text-2xl font-bold tracking-tight text-slate-900" />
          <p className="text-xs text-text-secondary mt-1">Create Student Academic Account</p>
        </div>

        {/* Step 1 Form */}
        <form onSubmit={handleRequestOtp} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="col-span-1">
              <label className="block text-sm font-medium text-text-primary mb-1">First Name</label>
              <input
                required
                type="text"
                placeholder="John"
                className="w-full p-2 border rounded bg-muted text-sm"
                value={formData.first_name}
                onChange={e => setFormData({ ...formData, first_name: e.target.value })}
              />
            </div>
            <div className="col-span-1">
              <label className="block text-sm font-medium text-text-primary mb-1">Middle Name</label>
              <input
                type="text"
                placeholder="(Optional)"
                className="w-full p-2 border rounded bg-muted text-sm"
                value={formData.middle_name}
                onChange={e => setFormData({ ...formData, middle_name: e.target.value })}
              />
            </div>
            <div className="col-span-1">
              <label className="block text-sm font-medium text-text-primary mb-1">Last Name</label>
              <input
                required
                type="text"
                placeholder="Doe"
                className="w-full p-2 border rounded bg-muted text-sm"
                value={formData.last_name}
                onChange={e => setFormData({ ...formData, last_name: e.target.value })}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-1">Recovery Email ID (For Verification & Recovery)</label>
            <input
              required
              type="email"
              placeholder="student@example.com"
              className="w-full p-2 border rounded bg-muted text-sm"
              value={formData.recovery_email}
              onChange={e => setFormData({ ...formData, recovery_email: e.target.value })}
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-text-primary mb-1">Enrollment No.</label>
              <input
                required
                type="text"
                placeholder="e.g. 2023CSD0517"
                className="w-full p-2 border rounded bg-muted uppercase text-sm"
                value={formData.enrollment}
                onChange={handleEnrollmentChange}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-primary mb-1">Branch</label>
              <select
                className="w-full p-2 border rounded bg-muted text-sm"
                value={formData.branch}
                onChange={e => setFormData({ ...formData, branch: e.target.value })}
              >
                <option value="CSE">CSE</option>
                <option value="ECE">ECE</option>
                <option value="ME">ME</option>
                <option value="EE">EE</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-1">Semester</label>
            <select
              className="w-full p-2 border rounded bg-muted text-sm"
              value={formData.semester}
              onChange={e => setFormData({ ...formData, semester: e.target.value })}
            >
              <option value="Semester-1">Semester 1</option>
              <option value="Semester-2">Semester 2</option>
              <option value="Semester-3">Semester 3</option>
              <option value="Semester-4">Semester 4</option>
              <option value="Semester-5">Semester 5</option>
              <option value="Semester-6">Semester 6</option>
              <option value="Semester-7">Semester 7</option>
              <option value="Semester-8">Semester 8</option>
            </select>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-text-primary mb-1">Password</label>
              <div className="relative">
                <input
                  required
                  type={showPassword ? "text" : "password"}
                  minLength={8}
                  placeholder="••••••••"
                  className="w-full p-2 pr-9 border rounded bg-muted text-sm"
                  value={formData.password}
                  onChange={e => setFormData({ ...formData, password: e.target.value })}
                />
                <button
                  type="button"
                  tabIndex={-1}
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 p-0.5 focus:outline-none transition-colors"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-text-primary mb-1">Confirm Password</label>
              <div className="relative">
                <input
                  required
                  type={showConfirmPassword ? "text" : "password"}
                  minLength={8}
                  placeholder="••••••••"
                  className="w-full p-2 pr-9 border rounded bg-muted text-sm"
                  value={formData.confirm_password}
                  onChange={e => setFormData({ ...formData, confirm_password: e.target.value })}
                />
                <button
                  type="button"
                  tabIndex={-1}
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 p-0.5 focus:outline-none transition-colors"
                  aria-label={showConfirmPassword ? "Hide password" : "Show password"}
                >
                  {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={formData.branch !== 'CSE' || sendingOtp}
            className="w-full bg-primary hover:bg-primary-hover disabled:opacity-50 text-white py-2.5 rounded font-medium transition-colors mt-4 text-sm shadow-sm flex items-center justify-center gap-2"
          >
            {sendingOtp ? (
              <>
                <Loader2 size={16} className="animate-spin" />
                <span>Sending Verification Code...</span>
              </>
            ) : (
              <span>Verify & Continue</span>
            )}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-text-secondary">
          Already have an account? <Link to="/login" className="text-accent hover:underline font-semibold">Log in</Link>
        </p>
      </div>

      {/* Step 2: Email OTP Verification Modal */}
      {showOtpModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4 animate-in fade-in duration-200">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl border border-slate-200 relative animate-in zoom-in-95 duration-150">
            <button
              onClick={() => setShowOtpModal(false)}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-700 p-1 rounded-lg transition-colors"
            >
              <X size={18} />
            </button>

            <div className="flex items-center gap-2 text-primary font-bold text-lg mb-1">
              <ShieldCheck size={22} className="text-accent" />
              <span>Verify Email Address</span>
            </div>
            <p className="text-xs text-slate-500 mb-5 leading-relaxed">
              We sent a 6-digit verification code to <strong className="text-slate-700">{maskedEmail}</strong>. Enter it below to complete your registration.
            </p>

            <form onSubmit={handleFinalSignup} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1 uppercase tracking-wider">
                  6-Digit Verification Code
                </label>
                <input
                  type="text"
                  maxLength={6}
                  placeholder="123456"
                  className="w-full p-3 border border-slate-300 rounded-lg text-center font-mono text-xl font-bold tracking-widest text-primary bg-slate-50 focus:bg-white focus:border-primary outline-none transition-all"
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, ''))}
                  required
                  autoFocus
                />
              </div>

              <div className="flex items-center justify-between pt-2">
                <button
                  type="button"
                  onClick={handleResendOtp}
                  disabled={cooldown > 0 || sendingOtp}
                  className="text-xs text-accent hover:underline flex items-center gap-1 font-medium disabled:opacity-50 disabled:no-underline"
                >
                  <RefreshCw size={12} className={sendingOtp ? "animate-spin" : ""} />
                  <span>{cooldown > 0 ? `Resend Code (${cooldown}s)` : "Resend Code"}</span>
                </button>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => setShowOtpModal(false)}
                    className="px-3 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors flex items-center gap-1"
                  >
                    <ArrowLeft size={14} />
                    <span>Edit Details</span>
                  </button>

                  <button
                    type="submit"
                    disabled={verifying || otpCode.length !== 6}
                    className="px-4 py-2 text-xs font-semibold bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg transition-all shadow-md flex items-center gap-1.5 disabled:opacity-50"
                  >
                    {verifying ? <Loader2 size={14} className="animate-spin" /> : <ShieldCheck size={14} />}
                    <span>Complete Signup</span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

