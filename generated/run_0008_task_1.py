"""
This script, gui_server.py, is designed to serve as a GUI server.
It handles requests from a graphical user interface (GUI) client,
provides necessary data, and manages the communication between the client and backend services.
"""

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

class GUIRequestHandler(BaseHTTPRequestHandler):
    """
    Handles incoming HTTP requests from the GUI client.
    """

    def do_GET(self):
        """
        Responds to GET requests with a simple HTML page.
        """
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = "<html><head><title>GUI Server</title></head>" \
                   "<body><h1>Welcome to the GUI Server!</h1></body></html>"
            self.wfile.write(html.encode('utf-8'))
        except Exception as e:
            print(f"Error handling GET request: {e}")
            self.send_error(500, str(e))

    def do_POST(self):
        """
        Responds to POST requests with a simple text message.
        """
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print(f"Received POST data: {post_data.decode('utf-8')}")

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            response = "POST request received"
            self.wfile.write(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling POST request: {e}")
            self.send_error(500, str(e))

def run(server_class=HTTPServer, handler_class=GUIRequestHandler, port=8000):
    """
    Runs the GUI server on the specified port.
    
    :param server_class: Class to use for creating the HTTP server.
    :param handler_class: Class to handle incoming requests.
    :param port: Port number on which the server will listen.
    """
    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print(f"Starting GUI server on port {port}...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping GUI server.")
        httpd.server_close()
    except Exception as e:
        print(f"Error starting the server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run()
