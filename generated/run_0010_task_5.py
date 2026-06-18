from flask import Flask, render_template_string

def create_app():
    """
    Create and configure a simple Flask application.
    
    Returns:
        app (Flask): The configured Flask application.
    """
    app = Flask(__name__)

    @app.route('/')
    def dashboard():
        """
        Render the dashboard page.
        
        Returns:
            str: HTML content for the dashboard.
        """
        return render_template_string('''
            <!doctype html>
            <html lang="en">
              <head>
                <meta charset="utf-8">
                <title>Dashboard</title>
              </head>
              <body>
                <h1>Welcome to the Dashboard!</h1>
                <p>This is a simple dashboard application.</p>
              </body>
            </html>
        ''')

    return app

def run_server():
    """
    Start the local server and deploy the dashboard application.
    
    This function will start a Flask development server on localhost at port 5000.
    """
    try:
        app = create_app()
        print("Starting local server on http://127.0.0.1:5000")
        app.run(host='127.0.0.1', port=5000, debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_server()
