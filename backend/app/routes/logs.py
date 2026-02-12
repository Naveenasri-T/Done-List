from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.log import Log
from app.schemas.log import LogCreate, LogResponse, LogCreateResponse
from app.utils.auth import get_current_user
from app.services.game_logic import (
    get_tree_emoji_for_level,
    calculate_points,
    calculate_level,
    update_daily_streak,
    update_weekly_streak,
    update_monthly_streak,
    check_milestones
)

router = APIRouter()


@router.post("", response_model=LogCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_log(
    log_data: LogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task log"""
    # Calculate points
    points = calculate_points(log_data.effort_level)
    
    # Get tree emoji based on current level
    tree_emoji = get_tree_emoji_for_level(current_user.current_level)
    
    # Create log
    log = Log(
        user_id=current_user.id,
        task_text=log_data.task_text,
        effort_level=log_data.effort_level,
        points_earned=points,
        tree_emoji=tree_emoji,
        date=date.today()
    )
    
    db.add(log)
    
    # Update user stats
    old_level = current_user.current_level
    current_user.total_points += points
    current_user.current_level = calculate_level(current_user.total_points)
    level_up = current_user.current_level > old_level
    
    # Update streaks
    daily_streak = update_daily_streak(current_user, date.today(), db)
    update_weekly_streak(current_user, date.today(), db)
    update_monthly_streak(current_user, date.today(), db)
    
    # Update last log date
    current_user.last_log_date = date.today()
    
    # Check for milestones
    milestone_earned = check_milestones(current_user, daily_streak.current_count, db)
    
    db.commit()
    db.refresh(log)
    db.refresh(current_user)
    db.refresh(daily_streak)
    
    return LogCreateResponse(
        log=LogResponse.model_validate(log),
        new_total_points=current_user.total_points,
        new_level=current_user.current_level,
        new_streak=daily_streak.current_count,
        level_up=level_up,
        milestone_earned=milestone_earned
    )


@router.get("", response_model=List[LogResponse])
async def get_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's logs (paginated)"""
    logs = db.query(Log).filter(
        Log.user_id == current_user.id
    ).order_by(Log.logged_at.desc()).offset(skip).limit(limit).all()
    
    return [LogResponse.model_validate(log) for log in logs]


@router.get("/today", response_model=List[LogResponse])
async def get_today_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get today's logs"""
    logs = db.query(Log).filter(
        Log.user_id == current_user.id,
        Log.date == date.today()
    ).order_by(Log.logged_at.desc()).all()
    
    return [LogResponse.model_validate(log) for log in logs]


@router.get("/week")
async def get_weekly_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get last 7 days of log data for weekly graph"""
    last_7_days = [date.today() - timedelta(days=i) for i in range(6, -1, -1)]
    
    weekly_data = []
    for day in last_7_days:
        total_points = db.query(func.sum(Log.points_earned)).filter(
            Log.user_id == current_user.id,
            Log.date == day
        ).scalar() or 0
        
        weekly_data.append({
            "date": day.isoformat(),
            "day": day.strftime("%a"),
            "points": total_points
        })
    
    return weekly_data


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(
    log_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a log (note: this doesn't recalculate streaks/points)"""
    log = db.query(Log).filter(
        Log.id == log_id,
        Log.user_id == current_user.id
    ).first()
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found"
        )
    
    db.delete(log)
    db.commit()
    
    return None
