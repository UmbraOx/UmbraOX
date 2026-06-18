from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# In-memory database simulation
database = {
    'users': []
}

def validate_user(user_data):
    """Validate user data."""
    if not isinstance(user_data.get('name'), str) or not user_data['name']:
        raise ValueError("Name must be a non-empty string.")
    if not isinstance(user_data.get('age'), int) or user_data['age'] < 0:
        raise ValueError("Age must be a non-negative integer.")

@app.route('/users', methods=['GET'])
def get_users():
    """Retrieve all users."""
    return jsonify(database['users']), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a user by ID."""
    user = next((user for user in database['users'] if user['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    try:
        user_data = request.get_json()
        validate_user(user_data)
        user_id = len(database['users']) + 1
        user_data['id'] = user_id
        database['users'].append(user_data)
        return jsonify(user_data), 201
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user."""
    try:
        user = next((user for user in database['users'] if user['id'] == user_id), None)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        user_data = request.get_json()
        validate_user(user_data)
        user.update(user_data)
        return jsonify(user), 200
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    global database
    initial_count = len(database['users'])
    database['users'] = [user for user in database['users'] if user['id'] != user_id]
    if len(database['users']) == initial_count:
        return jsonify({'error': 'User not found'}), 404
    return '', 204

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Handle HTTP exceptions."""
    response = e.get_response()
    response.data = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description
    }).data
    response.content_type = "application/json"
    return response

if __name__ == '__main__':
    app.run(debug=True)
