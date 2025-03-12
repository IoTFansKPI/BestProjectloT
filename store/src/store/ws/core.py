from fastapi import WebSocket
from logging import getLogger


logger = getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    def __call__(self, *args, **kwargs):
        return self

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Active connections: {len(self.active_connections)}")
        logger.info(f"New connection {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, *args, **kwargs):
        for connection in self.active_connections:
            await connection.send_json(*args, **kwargs)


manager = ConnectionManager()
