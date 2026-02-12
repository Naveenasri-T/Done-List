import uuid
from sqlalchemy import Column, String, Integer, Date, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database import Base


class Streak(Base):
    __tablename__ = "streaks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    streak_type = Column(String(20), nullable=False)
    current_count = Column(Integer, default=0)
    best_count = Column(Integer, default=0)
    
    started_at = Column(Date, nullable=True)
    last_updated = Column(Date, nullable=True)
    
    streak_metadata = Column(JSONB, default={})
    
    __table_args__ = (
        CheckConstraint("streak_type IN ('daily', 'weekly', 'monthly', 'yearly')", name="valid_streak_type"),
        UniqueConstraint('user_id', 'streak_type', name='unique_user_streak_type'),
    )
    
    def __repr__(self):
        return f"<Streak {self.streak_type}: {self.current_count}>"
