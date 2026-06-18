import sys
import json

try:
    from flask import Flask, request, jsonify
    using_flask = True
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    using_flask = False

def validate_input(data):
    """Validate the input data."""
    if not isinstance(data, dict) or 'name' not in data or not isinstance(data['name'], str):
        return False
    return True

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "message": "Hello, World!"
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        if not validate_input(post_data):
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {
                "error": "Invalid input"
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
            return
        
        response = {
            "message": f"Hello, {post_data['name']}!"
        }
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

if using_flask:
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def hello_world():
        """Return a greeting message."""
        return jsonify({"message": "Hello, World!"})

    @app.route('/greet', methods=['POST'])
    def greet():
        """Greet the user by name."""
        data = request.get_json()
        
        if not validate_input(data):
            return jsonify({"error": "Invalid input"}), 400
        
        return jsonify({"message": f"Hello, {data['name']}!"}), 201

    def run_flask_app():
        app.run(port=8000)

else:
    def run_http_server():
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        print("Starting basic web server on port 8000...")
        httpd.serve_forever()

if __name__ == "__main__":
    if using_flask:
        run_flask_app()
    else:
        run_http_server()
