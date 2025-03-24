from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from ws.core import manager

ws_router = APIRouter()


@ws_router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
