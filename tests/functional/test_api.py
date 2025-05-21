import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_create_task():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/tasks/", json={"title": "Test", "description": "Desc"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test"
    assert data["description"] == "Desc"

@pytest.mark.asyncio
async def test_get_tasks():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        await client.post("/tasks/", json={"title": "Task for get", "description": "Desc"})
        response = await client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(task["title"] == "Task for get" for task in data)

@pytest.mark.asyncio
async def test_update_task():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response_create = await client.post("/tasks/", json={"title": "Old Title", "description": "Old Desc"})
        task_id = response_create.json()["id"]
        response_update = await client.put(f"/tasks/{task_id}", json={"title": "New Title", "description": "New Desc"})
    assert response_update.status_code == 200
    updated_task = response_update.json()
    assert updated_task["title"] == "New Title"
    assert updated_task["description"] == "New Desc"

@pytest.mark.asyncio
async def test_delete_task():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response_create = await client.post("/tasks/", json={"title": "To Delete", "description": "Desc"})
        task_id = response_create.json()["id"]
        response_delete = await client.delete(f"/tasks/{task_id}")
    assert response_delete.status_code == 200
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response_delete_again = await client.delete(f"/tasks/{task_id}")
    assert response_delete_again.status_code == 404

@pytest.mark.asyncio
async def test_create_task_invalid_data():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/tasks/", json={})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_search_tasks():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        await client.post("/tasks/", json={"title": "Need to find", "description": "..."})
        await client.post("/tasks/", json={"title": "...", "description": "..."})
        response = await client.get("/tasks/search", params={"query": "Need"})
    assert response.status_code == 200
    data = response.json()
    assert any("Need to find" == task["title"] for task in data)
