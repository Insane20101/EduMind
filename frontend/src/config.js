/**
 * Centralized API Base URL configuration resolver.
 * Handles environment variables, dynamic local network IP resolution for mobile/tablet testing,
 * and fallback options.
 */

export const getApiBaseUrl = () => {
  // 1. Check environment variables (supports both VITE_API_BASE_URL and VITE_API_URL)
  const envUrl = import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL;
  if (envUrl && typeof envUrl === 'string' && envUrl.trim() !== '') {
    return envUrl.trim().replace(/\/+$/, '');
  }

  // 2. Dynamic local network IP detection for mobile/tablet/other device testing:
  // If accessing from another device via IP (e.g., http://192.168.1.15:5173),
  // automatically target the backend at http://192.168.1.15:8000.
  if (typeof window !== 'undefined' && window.location && window.location.hostname) {
    const hostname = window.location.hostname;
    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
      const protocol = window.location.protocol || 'http:';
      return `${protocol}//${hostname}:8000`;
    }
  }

  // 3. Default fallback for local development on single machine
  return 'http://localhost:8000';
};

export const getApiUrl = () => `${getApiBaseUrl()}/api`;
