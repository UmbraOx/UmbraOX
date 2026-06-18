import subprocess
import sys

# Check if Flask is installed and install it if not
try:
    import flask
except ImportError:
    print("Flask is not installed. Installing now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def process_data():
    """
    This endpoint processes data sent in a POST request.
    
    Request:
        JSON: {
            "key": "value"
        }
        
    Response:
        JSON: {
            "status": "success",
            "data": {
                "received_key": "value"
            }
        }
        
    Errors:
        400 - Bad Request if the request data is invalid.
    """
    
    # Validate the incoming request
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    
    if 'key' not in data:
        return jsonify({"error": "Missing 'key' in request body"}), 400
    
    # Process the data (this is a placeholder for actual processing)
    processed_data = {
        "received_key": data['key']
    }
    
    return jsonify({"status": "success", "data": processed_data}), 200

@app.errorhandler(Exception)
def handle_exception(e):
    """
    Handle any exceptions that occur during request processing.
    
    Response:
        JSON: {
            "error": "Description of the error"
        }
        
    Status Code: 500 - Internal Server Error
    """
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
