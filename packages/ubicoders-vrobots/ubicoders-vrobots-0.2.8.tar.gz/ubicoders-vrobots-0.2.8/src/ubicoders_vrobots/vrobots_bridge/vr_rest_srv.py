from fastapi import FastAPI
import uvicorn
import websockets
import json
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware


async def check_alive(uri):
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(b"ping")
            response = await websocket.recv()
            return response == b"pong"

    except websockets.exceptions.ConnectionClosed:
        return False


# Example FastAPI app definition
def create_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*"
        ],  # Allows all origins, replace with your specific origins in production
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    @app.get("/")
    async def default():
        return "ok"

    @app.get("/ping")
    async def default():
        uri = "ws://localhost:12740"  # Replace with your server URI
        try:
            alive = await check_alive(uri)
            if alive:
                return {"status": 1, "data": None, "msg": "ok"}
            else:
                return {"status": 0, "data": None, "msg": "unreachable"}
        except Exception as e:
            return {"status": -1, "data": None, "msg": "error"}

    return app


# Function to run a FastAPI app with uvicorn programmatically
def run_server(port=12741):
    app = create_app()
    config = uvicorn.Config(
        app=app, host="0.0.0.0", port=port, loop="asyncio", log_level="warning"
    )
    server = uvicorn.Server(config)
    # print(f"\033[92mVRobot HC server is running @ port {port}\033[0m")
    server.run()


if __name__ == "__main__":
    run_server()
