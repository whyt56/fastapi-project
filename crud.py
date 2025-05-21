from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Task
from schemas import TaskCreate

def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session):
    return db.query(Task).all()

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db: Session, task_id: int, task: TaskCreate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.title = task.title
        db_task.description = task.description
        db_task.status = task.status
        db_task.priority = task.priority
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def search_tasks(db: Session, query: str):
    return db.query(Task).filter(
        or_(
            Task.title.ilike(f"%{query}%"),
            Task.description.ilike(f"%{query}%")
        )
    ).all()

def sort_tasks(db: Session, sort_by: str):
    if sort_by == "status":
        return db.query(Task).order_by(Task.status).all()
    elif sort_by == "created_at":
        return db.query(Task).order_by(Task.created_at).all()
    elif sort_by == "priority":
        return db.query(Task).order_by(Task.priority).all()
    return db.query(Task).all()

def get_top_priority_tasks(db: Session, limit: int):
    return db.query(Task).order_by(Task.priority.asc()).limit(limit).all()


