from typing import Annotated, List

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
