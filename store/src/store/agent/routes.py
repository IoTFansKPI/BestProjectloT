from typing import List, Annotated

from fastapi import APIRouter, Depends

from agent.schemas import ProcessedAgentData, ProcessedAgentDataInDB
from agent.service import AgentService

from ws.core import manager

agent_router = APIRouter()

AgentService = Annotated[AgentService, Depends()]


@agent_router.post("/")
async def create_processed_agent_data(
    data: List[ProcessedAgentData], service: AgentService
):
    results = await service.create_processed_data(
        [ProcessedAgentDataInDB(**el.model_dump_flat()) for el in data]
    )
    await manager.broadcast([result.model_dump(mode="json") for result in results])


@agent_router.get(
    "/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB,
)
async def read_processed_agent_data(
    processed_agent_data_id: int, service: AgentService
):
    data = await service.getById(processed_agent_data_id)
    return data


@agent_router.get("/", response_model=List[ProcessedAgentDataInDB])
async def list_processed_agent_data(service: AgentService):
    data = await service.list_processed_data()
    return data


@agent_router.put(
    "/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB,
)
async def update_processed_agent_data(
    processed_agent_data_id: int, data: ProcessedAgentData, service: AgentService
):
    result = await service.updateById(
        processed_agent_data_id, ProcessedAgentDataInDB(**data.model_dump_flat())
    )
    return result


@agent_router.delete(
    "/{processed_agent_data_id}",
    status_code=204,
)
async def delete_processed_agent_data(
    processed_agent_data_id: int, service: AgentService
):
    await service.deleteById(processed_agent_data_id)
