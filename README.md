# 🌲 Forest Done Log

A gamified "done list": log what you finish each day and watch it grow into a forest.
Every task you log plants a tree, earns points, and keeps your streaks alive.

## Features

- 📝 **Task logging** with three effort levels: 🌱 Seed, 🌿 Sapling, 🌳 Oak
- 🎮 **Gamification**: points per task, levels every 500 points, rarer trees unlock as you level up
- 🔥 **Streaks** tracked daily, weekly, monthly and yearly
- 🏆 **Milestone badges** and a streak leaderboard
- 🌍 **Share your forest** with a public link that others can like
- 📤 **Export** your data as CSV or JSON
- 🔐 **Sign in** with email/password (JWT) or Google SSO

## Tech Stack

| Part     | Technology                                                      |
|----------|-----------------------------------------------------------------|
| Frontend | React 18, Vite, React Router, Axios, `@react-oauth/google`      |
| Backend  | FastAPI, SQLAlchemy 2.0, Pydantic, python-jose (JWT), passlib   |
| Database | PostgreSQL                                                      |
| Hosting  | Render (API + web service), GitHub Pages (static frontend)      |

## Project Structure

```
Done-List/
├── backend/      # FastAPI API: models, routes, game logic   → see backend/README.md
├── frontend/     # React + Vite web app                      → see frontend/README.md
├── render.yaml   # Render blueprint for backend + frontend
├── Procfile      # Start command for the API
├── deploy.sh     # Build frontend and push to gh-pages (macOS/Linux)
├── deploy.ps1    # Same, for Windows PowerShell
└── DEPLOYMENT.md # Step-by-step Render deployment guide
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 13+

### 1. Clone the repo

```bash
git clone git@github.com:Naveenasri-T/Done-List.git
cd Done-List
```

### 2. Run the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then set DATABASE_URL, SECRET_KEY, etc.
python create_tables.py
uvicorn app.main:app --reload --port 8000
```

API docs are available at http://localhost:8000/docs.

### 3. Run the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

## API Overview

All endpoints are under `/api/v1`:

| Area      | Prefix      | Examples                                         |
|-----------|-------------|--------------------------------------------------|
| Auth      | `/auth`     | `register`, `login`, `google`, `me`              |
| Logs      | `/logs`     | create, list, `today`, `week`, delete            |
| Streaks   | `/streaks`  | all streaks, `milestones`, `leaderboard`         |
| Sharing   | `/share`    | create link, view public forest, revoke, like    |
| Export    | `/export`   | `csv`, `json`                                    |

See [backend/README.md](backend/README.md) for the full endpoint list.

## Deployment

- **Backend + frontend on Render:** use `render.yaml`, or follow [DEPLOYMENT.md](DEPLOYMENT.md).
- **Frontend on GitHub Pages:** every push to `main` builds and deploys via `.github/workflows/deploy.yml`.

## License

[MIT](LICENSE)
