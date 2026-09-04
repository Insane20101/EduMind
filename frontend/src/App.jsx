import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Chatbar from './components/Chatbar';
import Homepage from './pages/Homepage';
import SubjectDashboard from './pages/SubjectDashboard';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Profile from './pages/Profile';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import { useAuth } from './store/useAuth';
import { useAdminAuth } from './store/useAdminAuth';
import { Toaster } from 'react-hot-toast';
import ErrorBoundary from './components/ErrorBoundary';

function ProtectedRoute({ children }) {
  const isAuthenticated = useAuth((state) => state.isAuthenticated);
  return isAuthenticated ? children : <Navigate to="/login" />;
}

function AdminProtectedRoute({ children }) {
  const isAuthenticated = useAdminAuth((state) => state.isAuthenticated);
  return isAuthenticated ? children : <Navigate to="/admin/login" />;
}

function AppShell({ children }) {
  return (
    <div className="min-h-screen flex flex-col bg-app text-text-primary font-sans">
      <Header />
      <main className="flex-1 relative">
        {children}
      </main>
      <Chatbar />
    </div>
  );
}

import { getApiBaseUrl } from './config';

function App() {
  React.useEffect(() => {
    // Non-blocking background health ping to pre-warm Render instance
    fetch(`${getApiBaseUrl()}/health`).catch(() => {});
  }, []);

  return (
    <BrowserRouter>
      <Toaster 
        position="top-center" 
        toastOptions={{
          className: 'font-sans text-sm rounded-2xl p-4 shadow-2xl border',
          style: {
            background: '#0f172a',
            color: '#f8fafc',
            border: '1px solid #334155',
            maxWidth: '480px',
            wordBreak: 'break-word',
            overflowWrap: 'anywhere'
          },
          error: {
            style: {
              background: '#0f172a',
              color: '#f87171',
              border: '1px solid #7f1d1d',
              maxWidth: '480px',
              wordBreak: 'break-word',
              overflowWrap: 'anywhere'
            },
            iconTheme: {
              primary: '#ef4444',
              secondary: '#ffffff',
            },
          },
          success: {
            style: {
              background: '#0f172a',
              color: '#4ade80',
              border: '1px solid #14532d',
              maxWidth: '480px',
              wordBreak: 'break-word',
              overflowWrap: 'anywhere'
            },
            iconTheme: {
              primary: '#22c55e',
              secondary: '#ffffff',
            },
          }
        }}
      />
      <Routes>
        <Route path="/login" element={<ErrorBoundary><Login /></ErrorBoundary>} />
        <Route path="/signup" element={<ErrorBoundary><Signup /></ErrorBoundary>} />
        <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
        <Route path="/admin/login" element={<ErrorBoundary><AdminLogin /></ErrorBoundary>} />
        <Route path="/admin/dashboard" element={
          <AdminProtectedRoute>
            <ErrorBoundary>
              <AdminDashboard />
            </ErrorBoundary>
          </AdminProtectedRoute>
        } />

        
        <Route path="/" element={
          <ProtectedRoute>
            <AppShell>
              <ErrorBoundary>
                <Homepage />
              </ErrorBoundary>
            </AppShell>
          </ProtectedRoute>
        } />
        
        <Route path="/chat" element={
          <ProtectedRoute>
            <AppShell>
              <ErrorBoundary>
                <SubjectDashboard />
              </ErrorBoundary>
            </AppShell>
          </ProtectedRoute>
        } />
        
        <Route path="/profile" element={
          <ProtectedRoute>
            <AppShell>
              <ErrorBoundary>
                <Profile />
              </ErrorBoundary>
            </AppShell>
          </ProtectedRoute>
        } />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}


export default App;
