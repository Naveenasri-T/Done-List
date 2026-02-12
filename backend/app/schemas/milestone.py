from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class MilestoneResponse(BaseModel):
    id: UUID
    user_id: UUID
    badge_name: str
    badge_type: str
    description: str | None = None
    earned_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
