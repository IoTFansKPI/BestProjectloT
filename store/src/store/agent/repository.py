from typing import List

from sqlalchemy import insert, select, delete, update

from agent.schemas import ProcessedAgentDataInDB
from database.core import DBSession
from agent.models import ProcessedAgent


class AgentRepository:
    def __init__(self, session: DBSession):
        self._session = session
        self._model = ProcessedAgent

    async def create(
        self, data: List[ProcessedAgentDataInDB]
    ) -> List[ProcessedAgentDataInDB]:
        results = await self._session.execute(
            insert(self._model).returning(self._model.id), data
        )
        await self._session.commit()
        inserted_ids = results.scalars().all()
        stmt = select(self._model).where(self._model.id.in_(inserted_ids))
        fetch_result = await self._session.execute(stmt)
        results = fetch_result.scalars().all()
        return (
            [ProcessedAgentDataInDB.model_validate(result) for result in results]
            if results
            else None
        )

    async def getAll(self) -> List[ProcessedAgentDataInDB]:
        stmt = select(self._model).order_by(self._model.id)
        result = await self._session.execute(stmt)
        results = result.scalars().all()
        return (
            [ProcessedAgentDataInDB.model_validate(result) for result in results]
            if results
            else None
        )

    async def getById(self, processed_agent_data_id: int) -> ProcessedAgentDataInDB:
        stmt = select(self._model).where(self._model.id == processed_agent_data_id)
        result = await self._session.execute(stmt)
        result = result.scalar_one_or_none()
        return ProcessedAgentDataInDB.model_validate(result) if result else None

    async def updateById(
        self, processed_agent_data_id, data: ProcessedAgentDataInDB
    ) -> ProcessedAgentDataInDB:
        stmt = (
            update(self._model)
            .where(self._model.id == processed_agent_data_id)
            .values(data.model_dump(exclude={"id"}))
            .returning(self._model.id)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        updated_instance = result.scalar_one_or_none()
        stmt = select(self._model).where(self._model.id == updated_instance)
        result = await self._session.execute(stmt)
        result = result.scalar_one_or_none()
        return ProcessedAgentDataInDB.model_validate(result) if result else None

    async def deleteById(self, processed_agent_data_id):
        stmt = delete(self._model).where(self._model.id == processed_agent_data_id)
        await self._session.execute(stmt)
        await self._session.commit()
