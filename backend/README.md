# 🌲 Forest Done Log - Backend API

FastAPI backend for the Forest Done Log application - A gamified task logging system with streaks, points, and visual forests.

## Features

- 🔐 JWT Authentication
- 📝 Task logging with effort levels (Seed, Sapling, Oak)
- 🔥 Multi-timeframe streaks (Daily, Weekly, Monthly, Yearly)
- 🎮 Gamification: Points, Levels, Tree unlocks
- 🏆 Milestone badges
- 🌍 Public forest sharing
- 📤 Data export (CSV/JSON)
- 📊 Leaderboards

## Tech Stack

- **Framework**: FastAPI 0.109+
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic

## Prerequisites

- Python 3.10+
- PostgreSQL 13+
- pip

## Installation

### 1. Clone and navigate to backend
```bash
cd backend
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
```

Required environment variables:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/forest_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 5. Create database
```bash
# Using psql
createdb forest_db

# Or using PostgreSQL client
psql -U postgres
CREATE DATABASE forest_db;
\q
```

### 6. Create database tables
```bash
python create_tables.py
```

### 7. Start the server
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user
- `PATCH /api/v1/auth/me` - Update user profile

### Logs
- `POST /api/v1/logs` - Create new task log
- `GET /api/v1/logs` - Get all logs (paginated)
- `GET /api/v1/logs/today` - Get today's logs
- `GET /api/v1/logs/week` - Get weekly momentum data
- `DELETE /api/v1/logs/{id}` - Delete a log

### Streaks
- `GET /api/v1/streaks` - Get all streaks
- `GET /api/v1/streaks/milestones` - Get earned badges
- `GET /api/v1/streaks/leaderboard` - Get top daily streaks

### Sharing
- `POST /api/v1/share` - Create share link
- `GET /api/v1/share/{token}` - View shared forest (public)
- `DELETE /api/v1/share/{token}` - Revoke share link
- `GET /api/v1/share` - Get my share links
- `POST /api/v1/share/{token}/like` - Like a shared forest

### Export
- `GET /api/v1/export/csv` - Export logs as CSV
- `GET /api/v1/export/json` - Export full data as JSON

## Database Schema

The application uses 7 main tables:
1. **users** - User accounts and stats
2. **logs** - Task entries
3. **streaks** - Multi-timeframe streak tracking
4. **milestones** - Earned badges
5. **shared_forests** - Public share links
6. **forest_likes** - Social engagement
7. **export_jobs** - Export tracking

## Development

### Create tables after model changes
```bash
python create_tables.py
```

### Run tests
```bash
pytest
```

### Run with hot reload
```bash
uvicorn app.main:app --reload --port 8000
```

## Project Structure

```
backend/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   ├── utils/           # Utilities (auth, etc.)
│   ├── main.py          # FastAPI app
│   ├── database.py      # Database connection
│   └── config.py        # Settings
├── tests/               # Test files
├── create_tables.py     # Database initialization
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```

## Deployment

### Using Railway/Render
1. Push code to GitHub
2. Connect repository to hosting service
3. Set environment variables
4. Deploy!

### Using Docker
```bash
# Build image
docker build -t forest-api .

# Run container
docker run -p 8000:8000 --env-file .env forest-api
```

## Security Notes

- Always use a strong `SECRET_KEY` in production
- Never commit `.env` file
- Use HTTPS in production
- Set `ENVIRONMENT=production` in production
- Enable rate limiting (already configured)

## License

MIT

## Support

For issues, please refer to the main project repository or create an issue on GitHub.
