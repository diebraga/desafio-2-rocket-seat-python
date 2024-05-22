import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"


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
    assert (task_id) == 0
    if task_id:
        get_response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert get_response.status_code == 200, f"Expected status code 200, but got {get_response.status_code}"
        created_task = get_response.json()
        assert created_task["title"] == new_task[0]
        assert created_task["description"] == new_task["description"]
        assert created_task["price"] == new_task["price"]


if __name__ == "__main__":
    pytest.main()
