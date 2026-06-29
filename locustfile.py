from locust import HttpUser, task, between

class TodoUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        response = self.client.post("/tasks", json={
            "title": "Tâche de test",
            "priority": "medium"
        })
        if response.status_code == 201:
            self.task_id = response.json()["id"]
        else:
            self.task_id = 1

    @task(3)
    def get_all_tasks(self):
        self.client.get("/tasks")

    @task(2)
    def create_task(self):
        self.client.post("/tasks", json={
            "title": "Nouvelle tâche",
            "priority": "high"
        })

    @task(1)
    def get_single_task(self):
        self.client.get(f"/tasks/{self.task_id}")