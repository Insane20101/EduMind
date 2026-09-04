import React from 'react';
import { User, LogOut } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../store/useAuth';

export default function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-50 h-16 bg-white border-b border-border-subtle flex items-center justify-between px-4 sm:px-6 lg:px-8">
      <Link to="/" className="text-xl font-semibold text-primary">
        EduMind
      </Link>
      <div className="flex items-center gap-4">
        {user && (
          <span className="text-sm font-medium text-text-secondary hidden sm:inline-block">
            {user.first_name} {user.last_name} ({user.branch})
          </span>
        )}
        <div className="flex items-center gap-2">
          <button 
            onClick={() => navigate('/profile')}
            className="h-10 w-10 rounded-full bg-muted flex items-center justify-center text-text-secondary hover:text-primary hover:bg-border-subtle transition-colors"
            title="Profile"
          >
            <User size={20} />
          </button>
          {user && (
            <button 
              onClick={handleLogout}
              className="h-10 w-10 rounded-full bg-muted flex items-center justify-center text-red-500 hover:bg-red-50 transition-colors"
              title="Logout"
            >
              <LogOut size={20} />
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
