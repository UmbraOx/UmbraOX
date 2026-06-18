from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

def get_system_status():
    """
    This function simulates retrieving the current status of the system.
    In a real-world scenario, this could involve checking database connectivity,
    service health, or other critical system components.
    
    Returns:
        dict: A dictionary representing the system status
    """
    # Simulated system status
    return {
        "system": "up",
        "database": "connected",
        "services": ["running", "running", "stopped"]
    }

@app.route('/api/status', methods=['GET'])
def api_status():
    """
    Endpoint to retrieve the current status of the system.

    Returns:
        JSON response with the system status and HTTP 200 OK.
    
    Raises:
        HTTPException: If an error occurs while retrieving the status.
    """
    try:
        # Retrieve the system status
        status = get_system_status()
        
        # Return the status as a JSON response
        return jsonify(status), 200
    
    except Exception as e:
        # Handle any unexpected errors and return a generic error message
        app.logger.error(f"Error retrieving system status: {e}")
        return jsonify({"error": "Unable to retrieve system status"}), 500

if __name__ == '__main__':
    app.run(debug=True)
