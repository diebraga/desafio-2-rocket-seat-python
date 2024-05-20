from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from models.task import Task
from typing import List

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


tasks: List[Task] = []  # type: ignore

task_id = 0


@app.route("/tasks", methods=["GET"])
def get_tasks():
    task_count = len(tasks)
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total_tasks": task_count
    }
    try:
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id
    try:
        received_task = request.get_json()
        new_task = Task(price=received_task["price"], title=received_task["title"],
                        description=received_task["description"], id=task_id)
        task_id = task_id + 1
        tasks.append(new_task)
        return jsonify(new_task.__dict__), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."}), 404


@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        "error": str(e)
    }
    return jsonify(response), 500


if __name__ == "__main__":
    app.run(debug=True)
