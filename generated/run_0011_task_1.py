from flask import Flask, jsonify, request
from pydantic import BaseModel, ValidationError
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Example models for request validation using Pydantic
class RunRequest(BaseModel):
    task_id: int
    parameters: dict

# In-memory storage for simplicity
history = []
metrics = {}

@app.route('/api/status', methods=['GET'])
def get_status():
    """
    Get the current status of the system.
    Returns:
        JSON response with a status message.
    """
    return jsonify({"status": "active"}), 200

@app.route('/api/run', methods=['POST'])
def run_task():
    """
    Run a task based on the provided parameters.
    Request Body:
        - task_id: int
        - parameters: dict
    Returns:
        JSON response with the result of the task or an error message.
    """
    try:
        data = RunRequest(**request.json)
        # Simulate running a task
        logging.info(f"Running task {data.task_id} with params {data.parameters}")
        result = {"task_id": data.task_id, "status": "completed"}
        return jsonify(result), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Get the history of executed tasks.
    Returns:
        JSON response with a list of task histories.
    """
    return jsonify(history), 200

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """
    Get system metrics.
    Returns:
        JSON response with system metrics.
    """
    return jsonify(metrics), 200

@app.route('/api/health', methods=['GET'])
def check_health():
    """
    Check the health of the API.
    Returns:
        JSON response indicating the health status.
    """
    return jsonify({"healthy": True}), 200

if __name__ == '__main__':
    app.run(debug=True)
