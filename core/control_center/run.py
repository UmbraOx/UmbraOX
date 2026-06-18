import uvicorn
from core.control_center.server import app

def start():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    start()