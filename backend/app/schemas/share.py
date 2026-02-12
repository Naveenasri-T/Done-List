from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional
from datetime import datetime
from uuid import UUID


class SharedForestCreate(BaseModel):
    share_type: Literal["profile", "weekly", "monthly"] = "profile"


class SharedForestResponse(BaseModel):
    id: UUID
    user_id: UUID
    share_token: str
    share_type: str
    is_active: bool
    view_count: int
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class PublicForestData(BaseModel):
    username: str
    total_points: int
    current_level: int
    daily_streak: int
    view_count: int
    recent_trees: list = []
