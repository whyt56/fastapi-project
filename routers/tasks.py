from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, schemas

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@router.get("/", response_model=list[schemas.TaskResponse])
def read_tasks(db: Session = Depends(get_db)) -> object:
    return crud.get_tasks(db)

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.update_task(db, task_id, task)

@router.delete("/{task_id}", response_model=schemas.TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return crud.delete_task(db, task_id)

@router.get("/search", response_model=list[schemas.TaskResponse])
def search_tasks(query: str, db: Session = Depends(get_db)):
    return crud.search_tasks(db, query)

@router.get("/sort", response_model=list[schemas.TaskResponse])
def sort_tasks(sort_by: str, db: Session = Depends(get_db)):
    return crud.sort_tasks(db, sort_by)
