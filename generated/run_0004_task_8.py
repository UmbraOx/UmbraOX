from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route('/api/greet', methods=['GET'])
def greet():
    """
    Greet a user by name.
    
    Query Parameters:
    - name: str (required) - The name of the user to greet.

    Returns:
    JSON response with a greeting message and HTTP status code 200.
    """
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    return jsonify({"message": f"Hello, {name}!"}), 200

@app.errorhandler(HTTPException)
def handle_exception(e):
    """
    Handle HTTP exceptions and return a JSON response with the error message.
    
    Returns:
    JSON response with an error message and the corresponding HTTP status code.
    """
    response = e.get_response()
    response.data = jsonify({"error": e.description})
    response.content_type = "application/json"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
