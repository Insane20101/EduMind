import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../store/useAuth';
import toast from 'react-hot-toast';

export default function Signup() {
  const [formData, setFormData] = useState({
    enrollment: '',
    email: '',
    branch: 'CSE',
    semester: 'Semester-3',
    first_name: '',
    middle_name: '',
    last_name: '',
    password: '',
    confirm_password: ''
  });
  
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleEnrollmentChange = (e) => {
    let val = e.target.value.toUpperCase();
    setFormData({...formData, enrollment: val});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.branch !== 'CSE') {
      toast.error(`Coming Soon for ${formData.branch}`);
      return;
    }
    if (formData.password !== formData.confirm_password) {
      toast.error('Passwords do not match');
      return;
    }
    
    try {
      const { confirm_password, ...submitData } = formData;
      await signup(submitData);
      toast.success('Account created successfully!');
      navigate('/');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Signup failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-app px-4 py-8">
      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-lg border border-border-subtle">
        <h2 className="text-2xl font-bold text-primary mb-6 text-center">Join EduMind</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="col-span-1">
              <label className="block text-sm font-medium text-text-primary mb-1">First Name</label>
              <input required type="text" placeholder="John" className="w-full p-2 border rounded bg-muted text-sm" value={formData.first_name} onChange={e => setFormData({...formData, first_name: e.target.value})} />
            </div>
            <div className="col-span-1">
              <label className="block text-sm font-medium text-text-primary mb-1">Middle Name</label>
              <input type="text" placeholder="(Optional)" className="w-full p-2 border rounded bg-muted text-sm" value={formData.middle_name} onChange={e => setFormData({...formData, middle_name: e.target.value})} />
            </div>
            <div className="col-span-1">
              <label className="block text-sm font-medium text-text-primary mb-1">Last Name</label>
              <input required type="text" placeholder="Doe" className="w-full p-2 border rounded bg-muted text-sm" value={formData.last_name} onChange={e => setFormData({...formData, last_name: e.target.value})} />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-1">Email Address (For Password Reset OTP)</label>
            <input required type="email" placeholder="student@example.com" className="w-full p-2 border rounded bg-muted text-sm" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-text-primary mb-1">Enrollment No.</label>
              <input required type="text" placeholder="e.g. 2023CSE0123" className="w-full p-2 border rounded bg-muted uppercase text-sm" value={formData.enrollment} onChange={handleEnrollmentChange} />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-primary mb-1">Branch</label>
              <select className="w-full p-2 border rounded bg-muted text-sm" value={formData.branch} onChange={e => setFormData({...formData, branch: e.target.value})}>
                <option value="CSE">CSE</option>
                <option value="ECE">ECE</option>
                <option value="ME">ME</option>
                <option value="EE">EE</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-1">Semester</label>
            <select className="w-full p-2 border rounded bg-muted text-sm" value={formData.semester} onChange={e => setFormData({...formData, semester: e.target.value})}>
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
              <input required type="password" minLength={8} placeholder="••••••••" className="w-full p-2 border rounded bg-muted text-sm" value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})} />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-primary mb-1">Confirm Password</label>
              <input required type="password" minLength={8} placeholder="••••••••" className="w-full p-2 border rounded bg-muted text-sm" value={formData.confirm_password} onChange={e => setFormData({...formData, confirm_password: e.target.value})} />
            </div>
          </div>

          <button type="submit" disabled={formData.branch !== 'CSE'} className="w-full bg-primary hover:bg-primary-hover disabled:opacity-50 text-white py-2.5 rounded font-medium transition-colors mt-4 text-sm shadow-sm">
            Sign Up
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-text-secondary">
          Already have an account? <Link to="/login" className="text-accent hover:underline font-semibold">Log in</Link>
        </p>
      </div>
    </div>
  );
}
