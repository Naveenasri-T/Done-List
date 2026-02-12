import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class Milestone(Base):
    __tablename__ = "milestones"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    badge_name = Column(String(100), nullable=False)
    badge_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Milestone {self.badge_name}>"
