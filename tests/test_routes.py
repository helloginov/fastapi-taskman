from fastapi.testclient import TestClient
import faker 
from app.main import app  # Assuming your FastAPI app is defined in app/main.py

client = TestClient(app)
fake = faker.Faker()

client.fake_user_email = fake.email()
client.fake_user_password = fake.password()
client.fake_user_name = fake.first_name()

def test_create_project():
    """
    Test creating a new project.
    """
    project_data = {
        "name": fake.word(),
        "description": fake.sentence(),
    }
    response = client.post("/tasks/new_project", json=project_data)
    assert response.status_code == 201
    assert response.json()["name"] == project_data["name"]
    assert response.json()["description"] == project_data["description"]

def test_get_all_projects():
    """
    Test retrieving all projects.
    """
    response = client.get("/tasks/all_projects")
    assert response.status_code in [200, 204]  # 204 if no projects exist
    if response.status_code == 200:
        assert isinstance(response.json(), list)


def test_create_task():
    """
    Test creating a new task.
    """
    user_response = client.post(
        "/auth/signup",
        json={"email": client.fake_user_email,
              "password": client.fake_user_password,
              "name": client.fake_user_name}
    )
    # First, create a project to associate the task with
    project_data = {
        "name": fake.word(),
        "description": fake.sentence(),
    }
    project_response = client.post("/tasks/new_project", json=project_data)
    project_id = project_response.json()["id"]
    

    # Create a task
    task_data = {
        "description": fake.sentence(),
        "assignee": client.fake_user_name,
        "due_date": "2030-01-01",
        "project": project_id,
        "complexity": fake.random_int(min=1, max=5),
    }
    response = client.post("/tasks/new_task", json=task_data)
    try:
        assert response.status_code == 201
        assert response.json()["description"] == task_data["description"]
    except AssertionError:
        raise AssertionError(f"Response: {response.json()}")


def test_get_tasks_without_project():
    """
    Test retrieving tasks without a project.
    """
    response = client.get("/tasks/no_project")
    assert response.status_code in [200, 204]  # 204 if no tasks exist
    if response.status_code == 200:
        assert isinstance(response.json(), list)