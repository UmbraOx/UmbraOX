import asyncio
import websockets
import pandas as pd

# Sample data for demonstration purposes
data = {
    'A': [1, 2, None, 4],
    'B': [None, 3, 5, 6],
    'C': [7, 8, 9, None]
}

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(data)

# Function to handle WebSocket connections
async def handler(websocket, path):
    print("Client connected")

    # Handle missing data by filling NaN values with the mean of each column
    df_filled = df.fillna(df.mean())

    # Detect column types
    column_types = {col: str(dtype) for col, dtype in df_filled.dtypes.items()}
    print("Column Types:", column_types)

    # Stream data row by row to the client
    for index, row in df_filled.iterrows():
        formatted_row = row.to_dict()
        await websocket.send(f"Row {index}: {formatted_row}")

    print("Streaming complete. Client disconnected.")

# Start the WebSocket server
async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
