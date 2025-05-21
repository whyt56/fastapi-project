from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_tasks(self):
        self.client.get("/tasks/")

    @task(1)
    def create_task(self):
        self.client.post("/tasks/", json={"title": "Load Test Task", "description": "Testing load"})

    @task(2)
    def search_tasks(self):
        self.client.get("/tasks/search?query=Load")
