from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import secrets
from app.database import get_db
from app.models.user import User
from app.models.shared_forest import SharedForest
from app.models.forest_like import ForestLike
from app.models.streak import Streak
from app.models.log import Log
from app.schemas.share import SharedForestCreate, SharedForestResponse, PublicForestData
from app.utils.auth import get_current_user
from datetime import date, timedelta

router = APIRouter()


def generate_share_token() -> str:
    """Generate a random 8-character share token"""
    return secrets.token_urlsafe(6)[:8]


@router.post("", response_model=SharedForestResponse, status_code=status.HTTP_201_CREATED)
async def create_share_link(
    share_data: SharedForestCreate = SharedForestCreate(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a public share link"""
    if not current_user.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Profile must be public to share"
        )
    
    # Generate unique token
    token = generate_share_token()
    while db.query(SharedForest).filter(SharedForest.share_token == token).first():
        token = generate_share_token()
    
    share = SharedForest(
        user_id=current_user.id,
        share_token=token,
        share_type=share_data.share_type
    )
    
    db.add(share)
    db.commit()
    db.refresh(share)
    
    return SharedForestResponse.model_validate(share)


@router.get("/{token}", response_model=PublicForestData)
async def get_shared_forest(token: str, db: Session = Depends(get_db)):
    """View a shared forest (public endpoint)"""
    share = db.query(SharedForest).filter(
        SharedForest.share_token == token,
        SharedForest.is_active == True
    ).first()
    
    if not share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share link not found or inactive"
        )
    
    # Increment view count
    share.view_count += 1
    db.commit()
    
    # Get user data
    user = db.query(User).filter(User.id == share.user_id).first()
    
    # Get daily streak
    daily_streak = db.query(Streak).filter(
        Streak.user_id == user.id,
        Streak.streak_type == "daily"
    ).first()
    
    # Get recent trees (last 7 days)
    week_ago = date.today() - timedelta(days=6)
    recent_logs = db.query(Log).filter(
        Log.user_id == user.id,
        Log.date >= week_ago
    ).order_by(Log.logged_at.desc()).limit(20).all()
    
    return PublicForestData(
        username=user.username,
        total_points=user.total_points,
        current_level=user.current_level,
        daily_streak=daily_streak.current_count if daily_streak else 0,
        view_count=share.view_count,
        recent_trees=[
            {
                "tree": log.tree_emoji,
                "date": log.date.isoformat(),
                "points": log.points_earned
            }
            for log in recent_logs
        ]
    )


@router.delete("/{token}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_share_link(
    token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Revoke a share link"""
    share = db.query(SharedForest).filter(
        SharedForest.share_token == token,
        SharedForest.user_id == current_user.id
    ).first()
    
    if not share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share link not found"
        )
    
    share.is_active = False
    db.commit()
    
    return None


@router.get("", response_model=list[SharedForestResponse])
async def get_my_shares(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user's share links"""
    shares = db.query(SharedForest).filter(
        SharedForest.user_id == current_user.id
    ).order_by(SharedForest.created_at.desc()).all()
    
    return [SharedForestResponse.model_validate(s) for s in shares]


@router.post("/{token}/like", status_code=status.HTTP_201_CREATED)
async def like_shared_forest(
    token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Like a shared forest"""
    share = db.query(SharedForest).filter(
        SharedForest.share_token == token,
        SharedForest.is_active == True
    ).first()
    
    if not share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share link not found"
        )
    
    # Check if already liked
    existing_like = db.query(ForestLike).filter(
        ForestLike.shared_forest_id == share.id,
        ForestLike.liker_user_id == current_user.id
    ).first()
    
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already liked"
        )
    
    like = ForestLike(
        shared_forest_id=share.id,
        liker_user_id=current_user.id
    )
    
    db.add(like)
    db.commit()
    
    return {"message": "Liked successfully"}
