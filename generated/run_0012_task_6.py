import asyncio
import websockets

class WebSocketServer:
    """
    A simple WebSocket server implementation optimized for performance and reliability.
    
    This server handles incoming connections, manages them, and ensures that messages are
    delivered reliably to all connected clients.
    """

    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.clients = set()

    async def register(self, websocket: websockets.WebSocketServerProtocol) -> None:
        """
        Register a new client connection.
        
        :param websocket: The WebSocket connection to register.
        """
        self.clients.add(websocket)
        print(f"New client connected: {websocket.remote_address}")

    async def unregister(self, websocket: websockets.WebSocketServerProtocol) -> None:
        """
        Unregister a client connection when it closes or disconnects.
        
        :param websocket: The WebSocket connection to unregister.
        """
        self.clients.remove(websocket)
        print(f"Client disconnected: {websocket.remote_address}")

    async def broadcast(self, message: str) -> None:
        """
        Broadcast a message to all connected clients.
        
        This method ensures that the message is sent to each client in an asynchronous manner,
        which helps maintain performance and reliability.
        
        :param message: The message to broadcast.
        """
        if not self.clients:
            print("No clients connected.")
            return

        await asyncio.gather(*(client.send(message) for client in self.clients))

    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None:
        """
        Handle communication with a single client.
        
        This method registers the client, listens for incoming messages, and unregisters the
        client when the connection is closed.
        
        :param websocket: The WebSocket connection to handle.
        :param path: The request path (not used in this implementation).
        """
        await self.register(websocket)
        try:
            async for message in websocket:
                print(f"Received message from {websocket.remote_address}: {message}")
                await self.broadcast(message)
        except websockets.ConnectionClosedError:
            print(f"Connection closed by client: {websocket.remote_address}")
        finally:
            await self.unregister(websocket)

    def start(self) -> None:
        """
        Start the WebSocket server.
        
        This method sets up the server to listen for incoming connections and handle them using
        asyncio's event loop.
        """
        start_server = websockets.serve(
            handler=self.handle_client,
            host=self.host,
            port=self.port
        )
        print(f"WebSocket server started on ws://{self.host}:{self.port}")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    server = WebSocketServer()
    server.start()
