from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Sample data to simulate a log of past actions or events
history_log = [
    {"id": 1, "action": "User logged in", "timestamp": "2023-10-01T12:00:00Z"},
    {"id": 2, "action": "Order placed", "timestamp": "2023-10-01T12:05:00Z"},
    # Add more entries as needed
]

@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Retrieve the log of past actions or events.

    Returns:
        A JSON response with a list of history logs.
    """
    try:
        return jsonify(history_log), 200
    except Exception as e:
        app.logger.error(f"Error retrieving history: {e}")
        return jsonify({"error": "Failed to retrieve history"}), 500

@app.route('/api/history', methods=['POST'])
def add_history():
    """
    Add a new entry to the history log.

    Request Body:
        - action (str): The description of the action.
        - timestamp (str, optional): The timestamp of the action. Defaults to current time if not provided.

    Returns:
        A JSON response with the newly added history entry.
    """
    try:
        data = request.get_json()
        
        # Validate request
        if 'action' not in data or not isinstance(data['action'], str):
            return jsonify({"error": "Invalid action"}), 400
        
        new_entry = {
            "id": len(history_log) + 1,
            "action": data['action'],
            "timestamp": data.get('timestamp', None)
        }
        
        history_log.append(new_entry)
        return jsonify(new_entry), 201
    except Exception as e:
        app.logger.error(f"Error adding to history: {e}")
        return jsonify({"error": "Failed to add to history"}), 500

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """
    Handle HTTP exceptions globally.

    Args:
        e (HTTPException): The exception raised.

    Returns:
        A JSON response with the error message and status code.
    """
    return jsonify({"error": str(e)}), e.code

if __name__ == '__main__':
    app.run(debug=True)
