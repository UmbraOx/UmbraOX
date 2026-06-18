from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/check-flask', methods=['GET'])
def check_flask():
    """
    Check if Flask is installed on the system.

    Returns:
        JSON response with a status code and message indicating whether Flask is installed.
    """
    try:
        # Attempt to import flask to check if it's installed
        __import__('flask')
        return jsonify({"installed": True, "message": "Flask is installed."}), 200
    except ImportError:
        # If an ImportError occurs, Flask is not installed
        return jsonify({"installed": False, "message": "Flask is not installed."}), 404

if __name__ == '__main__':
    app.run(debug=True)
