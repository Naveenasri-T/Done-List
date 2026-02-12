from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.streak import Streak
from app.models.milestone import Milestone
from app.schemas.streak import StreakResponse, AllStreaksResponse
from app.schemas.milestone import MilestoneResponse
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("", response_model=AllStreaksResponse)
async def get_all_streaks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user streaks"""
    streaks = db.query(Streak).filter(Streak.user_id == current_user.id).all()
    
    result = AllStreaksResponse()
    for streak in streaks:
        streak_data = StreakResponse.model_validate(streak)
        setattr(result, streak.streak_type, streak_data)
    
    return result


@router.get("/milestones", response_model=List[MilestoneResponse])
async def get_milestones(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all earned milestones"""
    milestones = db.query(Milestone).filter(
        Milestone.user_id == current_user.id
    ).order_by(Milestone.earned_at.desc()).all()
    
    return [MilestoneResponse.model_validate(m) for m in milestones]


@router.get("/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    """Get daily streak leaderboard (top 10 public users)"""
    from sqlalchemy import desc
    
    leaderboard = db.query(
        User.username,
        User.total_points,
        User.current_level,
        Streak.current_count.label("streak")
    ).join(
        Streak, (Streak.user_id == User.id) & (Streak.streak_type == "daily")
    ).filter(
        User.is_public == True
    ).order_by(desc(Streak.current_count)).limit(10).all()
    
    return [
        {
            "username": row.username,
            "total_points": row.total_points,
            "level": row.current_level,
            "daily_streak": row.streak
        }
        for row in leaderboard
    ]
