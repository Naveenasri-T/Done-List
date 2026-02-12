import uuid
from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class ForestLike(Base):
    __tablename__ = "forest_likes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shared_forest_id = Column(UUID(as_uuid=True), ForeignKey("shared_forests.id", ondelete="CASCADE"), nullable=False)
    liker_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('shared_forest_id', 'liker_user_id', name='unique_forest_like'),
    )
    
    def __repr__(self):
        return f"<ForestLike {self.id}>"
