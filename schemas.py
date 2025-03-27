from pydantic import BaseModel
from datetime import datetime
from models import Status


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: Status = Status.PENDING
    priority: int = 1


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

