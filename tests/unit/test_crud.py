from sqlalchemy.orm import Session
from models import Status
from schemas import TaskCreate
import crud

def test_create_task(session: Session):
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test",
        status=Status.PENDING,
        priority=2
    )
    task = crud.create_task(session, task_data)
    assert task.id is not None
    assert task.title == task_data.title
    assert task.status == task_data.status
    assert task.priority == task_data.priority

def test_get_tasks(session: Session):
    crud.create_task(session, TaskCreate(title="Task 1", description="Desc 1", status=Status.PENDING, priority=1))
    crud.create_task(session, TaskCreate(title="Task 2", description="Desc 2", status=Status.COMPLETED, priority=2))

    tasks = crud.get_tasks(session)
    assert len(tasks) >= 2
    titles = [task.title for task in tasks]
    assert "Task 1" in titles
    assert "Task 2" in titles

def test_update_task(session: Session):
    created = crud.create_task(session, TaskCreate(title="Update Me", description="Old", status=Status.PENDING, priority=1))
    updated_data = TaskCreate(title="Updated", description="New", status=Status.IN_PROGRESS, priority=3)
    updated = crud.update_task(session, created.id, updated_data)

    assert updated.title == "Updated"
    assert updated.description == "New"
    assert updated.status == Status.IN_PROGRESS
    assert updated.priority == 3

def test_delete_task(session: Session):
    created = crud.create_task(session, TaskCreate(title="Delete Me", description="...", status=Status.PENDING, priority=1))
    deleted = crud.delete_task(session, created.id)
    assert deleted.id == created.id
    tasks = crud.get_tasks(session)
    assert all(task.id != created.id for task in tasks)

def test_search_tasks(session: Session):
    crud.create_task(session, TaskCreate(title="Do hw", description="...", status=Status.PENDING, priority=1))
    crud.create_task(session, TaskCreate(title="Call mom", description="...", status=Status.PENDING, priority=2))

    results = crud.search_tasks(session, query="hw")
    assert len(results) >= 1
    assert any("hw" in task.title.lower() for task in results)

def test_sort_tasks_by_status(session: Session):
    crud.create_task(session, TaskCreate(title="Low", description="...", status=Status.COMPLETED, priority=2))
    crud.create_task(session, TaskCreate(title="High", description="...", status=Status.IN_PROGRESS, priority=3))

    tasks = crud.sort_tasks(session, sort_by="status")
    assert tasks[0].status <= tasks[-1].status

def test_sort_tasks_by_priority(session: Session):
    crud.create_task(session, TaskCreate(title="P1", description="...", status=Status.PENDING, priority=1))
    crud.create_task(session, TaskCreate(title="P3", description="...", status=Status.PENDING, priority=3))

    tasks = crud.sort_tasks(session, sort_by="priority")
    priorities = [task.priority for task in tasks]
    assert priorities == sorted(priorities)

def test_get_top_priority_tasks(session: Session):
    crud.create_task(session, TaskCreate(title="T1", description="...", status=Status.PENDING, priority=2))
    crud.create_task(session, TaskCreate(title="T2", description="...", status=Status.PENDING, priority=1))
    crud.create_task(session, TaskCreate(title="T3", description="...", status=Status.PENDING, priority=3))

    top = crud.get_top_priority_tasks(session, limit=2)
    assert len(top) == 2
    assert top[0].priority <= top[1].priority
