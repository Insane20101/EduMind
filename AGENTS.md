# EduMind Deployment & Architecture Directives

## Production Environment & Live URLs
- **Backend Deployment**: Render (`https://edumind-ebk1.onrender.com`)
- **Frontend Deployment**: Vercel (`https://edumind-five.vercel.app`)
- **Repository**: `https://github.com/Insane20101/EduMind.git` (`main` branch)

## Workflow & Deployment Policy
1. **Direct Production Deployment**: All verified feature updates, bug fixes, and pipeline improvements must be committed and pushed directly to `origin/main`.
2. **Auto-Deployment Triggers**: Pushing to `origin/main` automatically triggers production builds on both Render (backend) and Vercel (frontend).
3. **No Hardcoded Endpoints**: Always ensure frontend API calls use `import.meta.env.VITE_API_URL` or relative proxy paths configured for production.
