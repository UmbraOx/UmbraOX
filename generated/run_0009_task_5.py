from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/greet', methods=['GET'])
def greet():
    """
    Greet the user by name.
    
    Query Parameters:
    - name: The name of the person to greet. If not provided, defaults to 'Guest'.
    
    Returns:
    JSON response with a greeting message and status code 200.
    """
    name = request.args.get('name', 'Guest')
    return jsonify(message=f'Hello, {name}!'), 200

@app.route('/add', methods=['POST'])
def add():
    """
    Add two numbers provided in the JSON body.
    
    JSON Body:
    - num1: The first number (integer or float).
    - num2: The second number (integer or float).
    
    Returns:
    JSON response with the sum of the numbers and status code 200.
    
    Raises:
    JSON response with an error message and status code 400 if inputs are invalid.
    """
    try:
        data = request.get_json()
        num1 = data.get('num1')
        num2 = data.get('num2')

        if not (isinstance(num1, (int, float)) and isinstance(num2, (int, float))):
            raise ValueError("Both num1 and num2 must be numbers.")

        result = num1 + num2
        return jsonify(result=result), 200

    except Exception as e:
        return jsonify(error=str(e)), 400

@app.errorhandler(404)
def not_found_error(error):
    """
    Handle 404 Not Found errors.
    
    Returns:
    JSON response with an error message and status code 404.
    """
    return jsonify(error='Resource not found'), 404

if __name__ == '__main__':
    app.run(debug=True)
