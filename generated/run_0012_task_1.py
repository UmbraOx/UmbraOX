"""
This script demonstrates how to implement a simple WebSocket server using the `websockets` library in Python.
The server will echo back any message it receives from connected clients.
"""

import asyncio
import websockets

async def echo(websocket, path):
    """
    Handle incoming WebSocket connections and echo back received messages.

    Args:
        websocket (WebSocketServerProtocol): The WebSocket connection object.
        path (str): The request path.
    """
    try:
        async for message in websocket:
            # Echo the received message back to the client
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosedError:
        print("Client disconnected")

async def main():
    """
    Start the WebSocket server on localhost at port 8765.
    """
    async with websockets.serve(echo, "localhost", 8765):
        print("WebSocket server started at ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
