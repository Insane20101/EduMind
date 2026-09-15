import React, { useState, useEffect } from 'react';
import { User, LogOut, Sun, Moon } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../store/useAuth';
import EduMindLogo from './EduMindLogo';

export default function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [theme, setTheme] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('edumind_theme');
      if (saved) return saved;
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return 'light';
  });

  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem('edumind_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === 'dark' ? 'light' : 'dark'));
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-50 h-16 bg-white dark:bg-slate-900 border-b border-border-subtle dark:border-slate-800 flex items-center justify-between px-4 sm:px-6 lg:px-8 transition-colors duration-200">
      <Link to="/" className="flex items-center">
        <EduMindLogo size={32} />
      </Link>
      <div className="flex items-center gap-3 sm:gap-4">
        {user && (
          <span className="text-sm font-medium text-text-secondary dark:text-slate-300 hidden sm:inline-block">
            {user.first_name} {user.last_name} ({user.branch})
          </span>
        )}

        {/* Theme Switch Toggle Button */}
        <button
          onClick={toggleTheme}
          className="relative p-2 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-amber-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 flex items-center justify-center"
          title={theme === 'dark' ? 'Switch to Light Theme' : 'Switch to Dark Theme'}
          aria-label="Toggle dark/light theme"
        >
          {theme === 'dark' ? (
            <Sun size={20} className="text-amber-400 animate-spin-slow transition-transform duration-300" />
          ) : (
            <Moon size={20} className="text-indigo-600 transition-transform duration-300" />
          )}
        </button>

        <div className="flex items-center gap-2">
          <button 
            onClick={() => navigate('/profile')}
            className="h-10 w-10 rounded-full bg-muted dark:bg-slate-800 flex items-center justify-center text-text-secondary dark:text-slate-200 hover:text-primary dark:hover:text-white hover:bg-border-subtle dark:hover:bg-slate-700 transition-colors"
            title="Profile"
          >
            <User size={20} />
          </button>
          {user && (
            <button 
              onClick={handleLogout}
              className="h-10 w-10 rounded-full bg-muted dark:bg-slate-800 flex items-center justify-center text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 transition-colors"
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

