import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../store/useAuth';
import toast from 'react-hot-toast';
import { User, Save, ArrowLeft } from 'lucide-react';

export default function Profile() {
  const { user, getProfile, updateProfile } = useAuth();
  const [formData, setFormData] = useState({
    first_name: '',
    middle_name: '',
    last_name: '',
    semester: '',
  });
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    document.title = "EduMind — Student Profile";
    if (user) {
      setFormData({
        first_name: user.first_name || '',
        middle_name: user.middle_name || '',
        last_name: user.last_name || '',
        semester: user.semester || '',
      });
    } else {
      fetchProfile();
    }
  }, [user]);

  const fetchProfile = async () => {
    try {
      await getProfile();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to load profile');
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await updateProfile(formData);
      toast.success('Profile updated successfully!');
      setIsEditing(false);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to update profile');
    } finally {
      setIsLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <User size={48} className="mx-auto text-text-secondary mb-4" />
          <p className="text-text-secondary">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-4 sm:p-6 lg:p-8 bg-app">
      <div className="max-w-2xl mx-auto">
        <div className="mb-4">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-sm font-semibold text-slate-600 hover:text-primary transition-colors"
          >
            <ArrowLeft size={18} />
            <span>Back to Home</span>
          </Link>
        </div>

        <div className="bg-white rounded-xl shadow-md border border-border-subtle p-8">
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-2xl font-bold text-primary">Profile</h1>
            <button
              onClick={() => setIsEditing(!isEditing)}
              className="px-4 py-2 text-sm font-medium text-primary border border-border-subtle rounded hover:bg-muted transition-colors"
            >
              {isEditing ? 'Cancel' : 'Edit'}
            </button>
          </div>

          <form onSubmit={handleSave} className="space-y-6">
            {/* Enrollment & Branch - Unconditionally Read Only */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-text-primary mb-1">Enrollment No.</label>
                <input
                  type="text"
                  value={user.enrollment || ''}
                  disabled={true}
                  readOnly
                  className="w-full p-3 border rounded bg-gray-100 text-text-secondary cursor-not-allowed"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-primary mb-1">Branch</label>
                <input
                  type="text"
                  value={user.branch || ''}
                  disabled={true}
                  readOnly
                  className="w-full p-3 border rounded bg-gray-100 text-text-secondary cursor-not-allowed"
                />
              </div>
            </div>

            {/* Email ID - Unconditionally Read Only */}
            <div>
              <label className="block text-sm font-medium text-text-primary mb-1">Recovery Email ID</label>
              <input
                type="email"
                value={user.recovery_email || user.email || ''}
                disabled={true}
                readOnly
                className="w-full p-3 border rounded bg-gray-100 text-text-secondary cursor-not-allowed"
              />
            </div>

            {/* Name Fields */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-text-primary mb-1">First Name</label>
                <input
                  type="text"
                  value={formData.first_name}
                  onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                  disabled={!isEditing}
                  className={`w-full p-3 border rounded transition-colors ${isEditing ? 'bg-muted focus:outline-none focus:ring-2 focus:ring-primary' : 'bg-gray-50 text-text-secondary'}`}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-primary mb-1">Middle Name</label>
                <input
                  type="text"
                  value={formData.middle_name}
                  onChange={(e) => setFormData({...formData, middle_name: e.target.value})}
                  disabled={!isEditing}
                  className={`w-full p-3 border rounded transition-colors ${isEditing ? 'bg-muted focus:outline-none focus:ring-2 focus:ring-primary' : 'bg-gray-50 text-text-secondary'}`}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-primary mb-1">Last Name</label>
                <input
                  type="text"
                  value={formData.last_name}
                  onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                  disabled={!isEditing}
                  className={`w-full p-3 border rounded transition-colors ${isEditing ? 'bg-muted focus:outline-none focus:ring-2 focus:ring-primary' : 'bg-gray-50 text-text-secondary'}`}
                />
              </div>
            </div>

            {/* Semester Field */}
            <div>
              <label className="block text-sm font-medium text-text-primary mb-1">Semester</label>
              <select
                value={formData.semester}
                onChange={(e) => setFormData({...formData, semester: e.target.value})}
                disabled={!isEditing}
                className={`w-full p-3 border rounded transition-colors ${isEditing ? 'bg-muted focus:outline-none focus:ring-2 focus:ring-primary' : 'bg-gray-50 text-text-secondary'}`}
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

            {/* Save Button */}
            {isEditing && (
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-primary hover:bg-primary-hover disabled:opacity-50 text-white py-3 rounded font-medium transition-colors flex items-center justify-center gap-2"
              >
                <Save size={20} />
                {isLoading ? 'Saving...' : 'Save Changes'}
              </button>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}
