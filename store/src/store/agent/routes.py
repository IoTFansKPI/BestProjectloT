from typing import List

from fastapi import APIRouter

from agent.schemas import ProcessedAgentData, ProcessedAgentDataInDB

agent_router = APIRouter()


@agent_router.post("/processed_agent_data/")
async def create_processed_agent_data(data: List[ProcessedAgentData]):
    pass


@agent_router.get(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB,
)
def read_processed_agent_data(processed_agent_data_id: int):
    pass


@agent_router.get("/processed_agent_data/", response_model=list[ProcessedAgentDataInDB])
def list_processed_agent_data():
    pass


@agent_router.put(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB,
)
def update_processed_agent_data(processed_agent_data_id: int, data: ProcessedAgentData):
    pass


# Update data
@agent_router.delete(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB,
)
def delete_processed_agent_data(processed_agent_data_id: int):
    pass
