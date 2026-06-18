from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

# Dummy data for demonstration purposes
system_metrics = {
    "cpu_usage": 75,
    "memory_usage": 80,
    "disk_space": 90,
    "requests_per_minute": 120
}

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """
    Retrieve system performance metrics and statistics.

    Returns:
        JSON response with the following structure:
            {
                "cpu_usage": int,
                "memory_usage": int,
                "disk_space": int,
                "requests_per_minute": int
            }
    Raises:
        BadRequest: If there is an error in processing the request.
    """
    try:
        # Simulate fetching metrics from a data source
        return jsonify(system_metrics), 200
    except Exception as e:
        app.logger.error(f"Error fetching system metrics: {e}")
        return jsonify({"error": "Failed to retrieve system metrics"}), 500

@app.route('/api/metrics', methods=['POST'])
def update_metrics():
    """
    Update system performance metrics and statistics.

    Request Body:
        {
            "cpu_usage": int,
            "memory_usage": int,
            "disk_space": int,
            "requests_per_minute": int
        }

    Returns:
        JSON response with the updated metrics.
    Raises:
        BadRequest: If the request body is invalid or missing required fields.
    """
    try:
        # Validate and update metrics
        data = request.get_json()
        if not all(key in data for key in system_metrics.keys()):
            raise BadRequest("Missing one or more required fields")

        for key, value in data.items():
            if not isinstance(value, int):
                raise BadRequest(f"Invalid type for {key}. Expected integer.")

        # Simulate updating metrics
        system_metrics.update(data)
        return jsonify(system_metrics), 200
    except BadRequest as e:
        app.logger.error(f"Bad request: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error updating system metrics: {e}")
        return jsonify({"error": "Failed to update system metrics"}), 500

if __name__ == '__main__':
    app.run(debug=True)
