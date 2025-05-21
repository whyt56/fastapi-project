from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from fastapi import HTTPException

router = APIRouter(prefix="/tasks", tags=["tasks"])


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
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.delete_task(db, task_id)

@router.get("/search", response_model=list[schemas.TaskResponse])
def search_tasks(query: str, db: Session = Depends(get_db)):
    return crud.search_tasks(db, query)

@router.get("/sort", response_model=list[schemas.TaskResponse])
def sort_tasks(sort_by: str, db: Session = Depends(get_db)):
    return crud.sort_tasks(db, sort_by)

@router.get("/top-priority/", response_model=list[schemas.TaskResponse])
def get_top_priority_tasks(limit: int = Query(5, alias="limit"), db: Session = Depends(get_db)):
    return crud.get_top_priority_tasks(db, limit)