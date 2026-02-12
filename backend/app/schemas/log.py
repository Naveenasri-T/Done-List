from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional
from datetime import datetime, date
from uuid import UUID


class LogCreate(BaseModel):
    task_text: str = Field(..., min_length=3, max_length=500)
    effort_level: Literal["seed", "sapling", "oak"]


class LogResponse(BaseModel):
    id: UUID
    user_id: UUID
    task_text: str
    effort_level: str
    points_earned: int
    tree_emoji: str
    logged_at: datetime
    date: date
    
    model_config = ConfigDict(from_attributes=True)


class LogCreateResponse(BaseModel):
    log: LogResponse
    new_total_points: int
    new_level: int
    new_streak: int
    level_up: bool = False
    milestone_earned: Optional[str] = None


from typing import Optional
