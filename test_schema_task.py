from app.tasks.schemas import TaskResponse

class FakeTask:
    def __init__(self):
        self.id = "9bce7ec7-fae6-4c36-bdd8-6e3f19fe7914"
        self.title = "Test task"
        self.description = None
        self.status = "todo"
        self.due_date = None
        self.created_at = "2026-01-01T00:00:00Z"
        self.updated_at = "2026-01-01T00:00:00Z"

fake = FakeTask()
response = TaskResponse.model_validate(fake)
print(response)