import http.server
import socketserver

def run_local_server(port=8000):
    """
    Runs a local HTTP server to host a dashboard.

    Args:
        port (int): The port number on which to serve the dashboard. Defaults to 8000.
    """
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Serving HTTP on port {port}...")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_local_server()
