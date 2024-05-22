import pytest
import requests
from run import app


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client


BASE_URL = "http://127.0.0.1:5000"
tasks = []


def test_create_task():
    new_task = {
        "title": "Etudie Phyton",
        "description": "Api avec flask",
        "price": "22"
    }

    # Send the POST request to create a new task
    response = requests.post(f"{BASE_URL}/tasks", json=new_task)

    # Check if the response status code is 201 (Created)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

    # fetch the created task to verify its content
    task_id = response.json().get("id")
    assert task_id is not None

    tasks.append(task_id)


def test_get_tasks():
    # Send the GET request to view tasks
    response = requests.get(f"{BASE_URL}/tasks")

    # Check if the response status code is 200
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "total_tasks" in data
    assert "tasks" in data


def test_get_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")

        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        data = response.json()
        assert data.get("id") == task_id


def test_update_task():
    if tasks:
        task_id = tasks[0]

        updated_task = {
            "title": "Etudie Phyton Updated",
            "description": "Api avec flask Updated",
            "price": "22899900"
        }

        response = requests.put(
            f"{BASE_URL}/tasks/{task_id}", json=updated_task)
        assert response.status_code == 200

        data = response.json()

        assert data["title"] == updated_task["title"]
        assert data["description"] == updated_task["description"]
        assert data["price"] == updated_task["price"]


def test_delete_task():
    if tasks:
        task_id = tasks[0]

        response = requests.delete(
            f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["message"] == "item deleted"

        del_response = requests.delete(
            f"{BASE_URL}/tasks/{task_id}")
        assert del_response.status_code == 404

        del_data = del_response.json()
        assert del_data["error"] == "not found"


if __name__ == "__main__":
    pytest.main()
