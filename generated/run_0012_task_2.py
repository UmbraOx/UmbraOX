import asyncio
import websockets
import json
import time

class RealTimeDataServer:
    """
    WebSocket server that streams real-time data.
    """

    def __init__(self, port=8765):
        self.port = port
        self.clients = set()

    async def register(self, websocket):
        """Register a new client."""
        self.clients.add(websocket)
        print(f"Client {websocket.remote_address} connected.")

    async def unregister(self, websocket):
        """Unregister a client."""
        self.clients.remove(websocket)
        print(f"Client {websocket.remote_address} disconnected.")

    async def broadcast_data(self, data):
        """Broadcast data to all registered clients."""
        if self.clients:
            message = json.dumps(data)
            await asyncio.wait([client.send(message) for client in self.clients])

    async def handle_client(self, websocket, path):
        """Handle a new WebSocket connection."""
        await self.register(websocket)
        try:
            while True:
                # Simulate real-time data generation
                data = {"timestamp": time.time(), "value": self.generate_data()}
                await self.broadcast_data(data)
                await asyncio.sleep(1)  # Adjust the sleep time for desired frequency
        except websockets.exceptions.ConnectionClosedError:
            print(f"Client {websocket.remote_address} unexpectedly disconnected.")
        finally:
            await self.unregister(websocket)

    def generate_data(self):
        """Simulate data generation."""
        return {"type": "random", "value": round(time.time() * 100) % 100}

    async def start_server(self):
        """Start the WebSocket server."""
        async with websockets.serve(self.handle_client, "localhost", self.port):
            print(f"WebSocket server started on port {self.port}")
            await asyncio.Future()  # Run forever

if __name__ == "__main__":
    server = RealTimeDataServer()
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("Server shutting down.")
