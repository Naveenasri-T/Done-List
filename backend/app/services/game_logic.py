import random
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.streak import Streak
from app.models.milestone import Milestone


# Tree emoji mappings based on level
TREE_EMOJIS = {
    "common": ["🌲", "🌳", "🌿"],
    "uncommon": ["🌴", "🌵", "🎍"],
    "rare": ["🌸", "🍂", "🍄", "🍀"],
    "legendary": ["🎋", "🎐", "⛲"]
}

# Points range by effort level
EFFORT_POINTS = {
    "seed": (5, 15),
    "sapling": (20, 50),
    "oak": (60, 150)
}


def get_tree_emoji_for_level(level: int) -> str:
    """Get a random tree emoji based on user level"""
    pool = list(TREE_EMOJIS["common"])
    
    if level >= 3:
        pool += TREE_EMOJIS["uncommon"]
    if level >= 7:
        pool += TREE_EMOJIS["rare"]
    if level >= 15:
        pool += TREE_EMOJIS["legendary"]
    
    return random.choice(pool)


def calculate_points(effort_level: str) -> int:
    """Calculate random points based on effort level"""
    min_points, max_points = EFFORT_POINTS[effort_level]
    return random.randint(min_points, max_points)


def calculate_level(total_points: int) -> int:
    """Calculate level based on total points (500 points per level)"""
    return (total_points // 500) + 1


def update_daily_streak(user: User, log_date: date, db: Session) -> Streak:
    """Update daily streak logic"""
    streak = db.query(Streak).filter(
        Streak.user_id == user.id,
        Streak.streak_type == "daily"
    ).first()
    
    if not streak:
        streak = Streak(user_id=user.id, streak_type="daily")
        db.add(streak)
    
    last_log = user.last_log_date
    
    if last_log is None:
        # First ever log
        streak.current_count = 1
        streak.started_at = log_date
    elif log_date == last_log:
        # Same day, no change
        pass
    elif log_date == last_log + timedelta(days=1):
        # Consecutive day
        streak.current_count += 1
    elif log_date > last_log + timedelta(days=1):
        # Missed a day, reset
        streak.current_count = 1
        streak.started_at = log_date
    
    # Update best streak
    if streak.current_count > streak.best_count:
        streak.best_count = streak.current_count
    
    streak.last_updated = log_date
    
    return streak


def update_weekly_streak(user: User, log_date: date, db: Session) -> Streak:
    """Update weekly streak (user must log 5+ days in a week)"""
    from sqlalchemy import func, extract
    from app.models.log import Log
    
    streak = db.query(Streak).filter(
        Streak.user_id == user.id,
        Streak.streak_type == "weekly"
    ).first()
    
    if not streak:
        streak = Streak(user_id=user.id, streak_type="weekly")
        db.add(streak)
    
    # Get ISO week number
    current_week = log_date.isocalendar()[1]
    current_year = log_date.year
    
    # Count unique days logged this week
    week_start = log_date - timedelta(days=log_date.weekday())
    week_end = week_start + timedelta(days=6)
    
    days_logged = db.query(func.count(func.distinct(Log.date))).filter(
        Log.user_id == user.id,
        Log.date >= week_start,
        Log.date <= week_end
    ).scalar()
    
    # Store in metadata
    metadata = streak.streak_metadata or {}
    metadata["current_week"] = f"{current_year}-W{current_week:02d}"
    metadata["days_active_this_week"] = days_logged
    streak.streak_metadata = metadata
    
    # Check if week is complete and active (5+ days)
    if days_logged >= 5 and log_date.weekday() == 6:  # Sunday
        last_week = metadata.get("last_active_week")
        if last_week is None:
            streak.current_count = 1
        elif f"{current_year}-W{current_week - 1:02d}" == last_week:
            streak.current_count += 1
        else:
            streak.current_count = 1
        
        metadata["last_active_week"] = f"{current_year}-W{current_week:02d}"
        streak.streak_metadata = metadata
        
        if streak.current_count > streak.best_count:
            streak.best_count = streak.current_count
    
    streak.last_updated = log_date
    
    return streak


def update_monthly_streak(user: User, log_date: date, db: Session) -> Streak:
    """Update monthly streak (user must log at least once per month)"""
    streak = db.query(Streak).filter(
        Streak.user_id == user.id,
        Streak.streak_type == "monthly"
    ).first()
    
    if not streak:
        streak = Streak(user_id=user.id, streak_type="monthly")
        db.add(streak)
    
    current_month = log_date.strftime("%Y-%m")
    last_month = (streak.streak_metadata or {}).get("last_active_month")
    
    if last_month is None:
        streak.current_count = 1
        streak.started_at = log_date
    elif current_month == last_month:
        # Same month, no change
        pass
    else:
        # Check if consecutive month
        last_date = date.fromisoformat(f"{last_month}-01")
        if log_date.year == last_date.year and log_date.month == last_date.month + 1:
            streak.current_count += 1
        elif log_date.year == last_date.year + 1 and log_date.month == 1 and last_date.month == 12:
            streak.current_count += 1
        else:
            streak.current_count = 1
            streak.started_at = log_date
    
    metadata = streak.streak_metadata or {}
    metadata["last_active_month"] = current_month
    streak.streak_metadata = metadata
    
    if streak.current_count > streak.best_count:
        streak.best_count = streak.current_count
    
    streak.last_updated = log_date
    
    return streak


def check_milestones(user: User, daily_streak: int, db: Session) -> str | None:
    """Check and award milestones"""
    milestone_configs = [
        (3, "3-Day Starter", "streak", "Logged for 3 consecutive days"),
        (7, "7-Day Warrior", "streak", "Logged for 7 consecutive days"),
        (10, "10-Day Champion", "streak", "Logged for 10 consecutive days"),
        (30, "30-Day Legend", "streak", "Logged for 30 consecutive days"),
    ]
    
    for threshold, badge_name, badge_type, description in milestone_configs:
        if daily_streak == threshold:
            # Check if already earned
            existing = db.query(Milestone).filter(
                Milestone.user_id == user.id,
                Milestone.badge_name == badge_name
            ).first()
            
            if not existing:
                milestone = Milestone(
                    user_id=user.id,
                    badge_name=badge_name,
                    badge_type=badge_type,
                    description=description
                )
                db.add(milestone)
                return badge_name
    
    return None
