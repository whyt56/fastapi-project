from sqlalchemy import Column, Integer, String, DateTime, Enum
from database import Base
from datetime import datetime
from enum import Enum as PyEnum


class Status(str, PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(Enum(Status), default=Status.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    priority = Column(Integer, default=1)
