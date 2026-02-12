import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class SharedForest(Base):
    __tablename__ = "shared_forests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    share_token = Column(String(10), unique=True, nullable=False, index=True)
    share_type = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        CheckConstraint("share_type IN ('profile', 'weekly', 'monthly')", name="valid_share_type"),
    )
    
    def __repr__(self):
        return f"<SharedForest {self.share_token}>"
