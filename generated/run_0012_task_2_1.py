import asyncio
import websockets
import json

async def client():
    """WebSocket client that receives real-time data."""
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                print(f"Received data: {data}")
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed by the server.")
        except KeyboardInterrupt:
            print("Client shutting down.")

if __name__ == "__main__":
    try:
        asyncio.run(client())
    except KeyboardInterrupt:
        print("Client shutting down.")
