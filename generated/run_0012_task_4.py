python
import websocket
import threading

def on_message(ws, message):
    """
    This function is called when a new message is received from the WebSocket server.
    :param ws: WebSocketApp object
    :param message: The received message
    """
    print("Received message:", message)

def on_error(ws, error):
    """
    This function is called when an error occurs with the WebSocket connection.
    :param ws: WebSocketApp object
    :param error: The error that occurred
    """
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    """
    This function is called when the WebSocket connection is closed.
    :param ws: WebSocketApp object
    :param close_status_code: The status code for the closure
    :param close_msg: A message describing the closure
    """
    print("Connection closed")

def on_open(ws):
    """
    This function is called when the WebSocket connection is opened.
    :param ws: WebSocketApp object
    """
    print("Connection opened")
    # You can send a message to the server here if needed
    # ws.send("Hello, Server!")

def main():
    websocket.enableTrace(True)  # Enable tracing for debugging

    # Define the WebSocket URL of your server
    url = "ws://your-websocket-server-url"

    # Create a WebSocketApp object with necessary callbacks
    ws = websocket.WebSocketApp(url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # Start the WebSocket connection in a new thread
    wst = threading.Thread(target=ws.run_forever)
    wst.start()

if __name__ == "__main__":
    main()
