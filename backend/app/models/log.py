import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, Date, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class Log(Base):
    __tablename__ = "logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    task_text = Column(Text, nullable=False)
    effort_level = Column(String(20), nullable=False)
    points_earned = Column(Integer, nullable=False)
    tree_emoji = Column(String(10), nullable=False)
    
    logged_at = Column(DateTime(timezone=True), server_default=func.now())
    date = Column(Date, nullable=False, server_default=func.current_date(), index=True)
    
    __table_args__ = (
        CheckConstraint("char_length(task_text) >= 3 AND char_length(task_text) <= 500", name="task_text_length"),
        CheckConstraint("effort_level IN ('seed', 'sapling', 'oak')", name="valid_effort_level"),
    )
    
    def __repr__(self):
        return f"<Log {self.id}: {self.task_text[:30]}...>"
