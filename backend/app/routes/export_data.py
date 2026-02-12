from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import date
import csv
import json
import io
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.models.log import Log
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/csv")
async def export_csv(
    date_start: Optional[date] = Query(None),
    date_end: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export user logs as CSV"""
    # Query logs
    query = db.query(Log).filter(Log.user_id == current_user.id)
    
    if date_start:
        query = query.filter(Log.date >= date_start)
    if date_end:
        query = query.filter(Log.date <= date_end)
    
    logs = query.order_by(Log.date.desc()).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(["Date", "Day", "Task", "Effort", "Points", "Tree"])
    
    # Write data
    for log in logs:
        writer.writerow([
            log.date.isoformat(),
            log.date.strftime("%A"),
            log.task_text,
            log.effort_level.capitalize(),
            log.points_earned,
            log.tree_emoji
        ])
    
    # Prepare response
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=forest_export_{date.today().isoformat()}.csv"
        }
    )


@router.get("/json")
async def export_json(
    date_start: Optional[date] = Query(None),
    date_end: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export user logs as JSON"""
    from app.models.streak import Streak
    from app.models.milestone import Milestone
    
    # Query logs
    query = db.query(Log).filter(Log.user_id == current_user.id)
    
    if date_start:
        query = query.filter(Log.date >= date_start)
    if date_end:
        query = query.filter(Log.date <= date_end)
    
    logs = query.order_by(Log.date.desc()).all()
    
    # Get streaks
    streaks = db.query(Streak).filter(Streak.user_id == current_user.id).all()
    
    # Get milestones
    milestones = db.query(Milestone).filter(Milestone.user_id == current_user.id).all()
    
    # Build export data
    export_data = {
        "user": {
            "username": current_user.username,
            "email": current_user.email,
            "total_points": current_user.total_points,
            "current_level": current_user.current_level,
            "created_at": current_user.created_at.isoformat()
        },
        "streaks": {
            s.streak_type: {
                "current": s.current_count,
                "best": s.best_count,
                "started_at": s.started_at.isoformat() if s.started_at else None
            }
            for s in streaks
        },
        "milestones": [
            {
                "badge_name": m.badge_name,
                "badge_type": m.badge_type,
                "description": m.description,
                "earned_at": m.earned_at.isoformat()
            }
            for m in milestones
        ],
        "logs": [
            {
                "date": log.date.isoformat(),
                "day": log.date.strftime("%A"),
                "task": log.task_text,
                "effort": log.effort_level,
                "points": log.points_earned,
                "tree": log.tree_emoji,
                "logged_at": log.logged_at.isoformat()
            }
            for log in logs
        ],
        "exported_at": date.today().isoformat()
    }
    
    return StreamingResponse(
        iter([json.dumps(export_data, indent=2)]),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=forest_export_{date.today().isoformat()}.json"
        }
    )
