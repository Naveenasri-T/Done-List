from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.config import settings
from app.routes import auth, logs, streaks, share, export_data
from app.database import Base, engine

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Forest Done Log API - Gamified task logging with streaks"
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - Allow all origins for deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, update this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to create tables (REMOVE AFTER FIRST SUCCESSFUL DEPLOYMENT)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(logs.router, prefix=f"{settings.API_V1_PREFIX}/logs", tags=["Logs"])
app.include_router(streaks.router, prefix=f"{settings.API_V1_PREFIX}/streaks", tags=["Streaks"])
app.include_router(share.router, prefix=f"{settings.API_V1_PREFIX}/share", tags=["Sharing"])
app.include_router(export_data.router, prefix=f"{settings.API_V1_PREFIX}/export", tags=["Export"])


@app.get("/")
async def root():
    return {
        "message": "Forest Done Log API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
