# Backend Deployment Guide

## Deploy Backend to Render (FREE)

### 1. Create Render Account
- Go to https://render.com/
- Sign up with GitHub

### 2. Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Name: `done-list-db`
3. Select FREE plan
4. Click "Create Database"
5. Copy the "Internal Database URL" (starts with `postgresql://`)

### 3. Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `Naveenasri-T/Done-List`
3. Configure:
   - **Name**: `done-list-api`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: FREE

4. Add Environment Variables:
   - `DATABASE_URL` = (paste the Internal Database URL from step 2)
   - `SECRET_KEY` = `your-super-secret-key-change-this-in-production`
   - `CORS_ORIGINS` = `https://naveenasri-t.github.io`
   - `ENVIRONMENT` = `production`

5. Click "Create Web Service"

### 4. Wait for Deployment
- Takes 2-5 minutes
- Your backend URL will be: `https://done-list-api-xxxx.onrender.com`

### 5. Update Frontend
1. Edit `frontend/.env.production`
2. Update `VITE_API_URL` with your Render backend URL
3. Run `.\deploy.ps1` to redeploy frontend

## Test Backend
Visit: `https://your-backend-url.onrender.com/docs`
You should see the API documentation!

---

## Alternative: Run Backend Locally

For testing only:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

Then access at: http://127.0.0.1:8000
