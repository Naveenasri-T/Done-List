from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional, Dict, Any
from datetime import date
from uuid import UUID


class StreakResponse(BaseModel):
    id: UUID
    user_id: UUID
    streak_type: Literal["daily", "weekly", "monthly", "yearly"]
    current_count: int
    best_count: int
    started_at: Optional[date] = None
    last_updated: Optional[date] = None
    streak_metadata: Dict[str, Any] = {}
    
    model_config = ConfigDict(from_attributes=True)


class AllStreaksResponse(BaseModel):
    daily: Optional[StreakResponse] = None
    weekly: Optional[StreakResponse] = None
    monthly: Optional[StreakResponse] = None
    yearly: Optional[StreakResponse] = None
