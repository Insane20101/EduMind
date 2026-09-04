import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Note: The proxy is kept as a convenience fallback for local dev, 
    // but the intended architecture is to bypass it using VITE_API_BASE_URL 
    // so the code behaves identically in both local development and production.
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
