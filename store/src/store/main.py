from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent.routes import agent_router
from ws.routes import ws_router


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


app = FastAPI(debug=True, root_path="/api/v1")

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(ws_router, prefix="/ws", tags=["ws"])
app.include_router(
    agent_router, prefix="/processed_agent_data", tags=["processed_agent_data"]
)
