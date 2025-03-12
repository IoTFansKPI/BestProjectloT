from typing import Annotated, List

from fastapi import HTTPException
from fastapi.params import Depends

from agent.schemas import ProcessedAgentDataInDB
from agent.repository import AgentRepository
from logging import getLogger

logger = getLogger(__name__)


class AgentService:
    def __init__(self, repository: Annotated[AgentRepository, Depends()]):
        self._repository = repository

    async def create_processed_data(self, data: List[ProcessedAgentDataInDB]):
        results = await self._repository.create(data)
        return results

    async def list_processed_data(self):
        return await self._repository.getAll()

    async def getById(self, processed_agent_data_id):
        data = await self._repository.getById(processed_agent_data_id)
        if not data:
            raise HTTPException(status_code=404, detail="No such data")
        return data

    async def updateById(self, processed_agent_data_id, data: ProcessedAgentDataInDB):
        if not await self._repository.getById(processed_agent_data_id):
            raise HTTPException(status_code=404, detail="No such data")
        data = await self._repository.updateById(processed_agent_data_id, data)
        return data

    async def deleteById(self, processed_agent_data_id):
        if not await self._repository.getById(processed_agent_data_id):
            raise HTTPException(status_code=404, detail="No such data")
        await self._repository.deleteById(processed_agent_data_id)
