"""
This script sets up a basic development environment for a web application using Flask.
It initializes the project by creating a simple Flask app with a single route.
"""

from flask import Flask, jsonify

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    @app.route('/')
    def home():
        """
        Handle requests to the root URL.

        Returns:
            Response: A JSON response with a welcome message.
        """
        return jsonify(message="Welcome to the Flask App!")

    @app.errorhandler(404)
    def not_found_error(error):
        """
        Handle 404 Not Found errors.

        Args:
            error (Exception): The exception that caused the error.

        Returns:
            Response: A JSON response with an error message.
        """
        return jsonify(error=str(error)), 404

    @app.errorhandler(500)
    def internal_error(error):
        """
        Handle 500 Internal Server errors.

        Args:
            error (Exception): The exception that caused the error.

        Returns:
            Response: A JSON response with an error message.
        """
        return jsonify(error=str(error)), 500

    return app

if __name__ == '__main__':
    # Create the Flask application
    app = create_app()

    # Run the application in debug mode
    app.run(debug=True)
