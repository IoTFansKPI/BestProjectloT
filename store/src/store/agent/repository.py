from typing import List

from sqlalchemy import insert, select

from agent.schemas import ProcessedAgentDataInDB
from database.core import DBSession
from agent.models import ProcessedAgent


class AgentRepository:
    def __init__(self, session: DBSession):
        self._session = session
        self._model = ProcessedAgent

    async def create(self, data: List[ProcessedAgentDataInDB]):
        results = await self._session.execute(
            insert(self._model).returning(self._model.id), data
        )
        await self._session.commit()
        inserted_ids = results.scalars().all()
        if not inserted_ids:
            return None
        stmt = select(self._model).where(self._model.id.in_(inserted_ids))
        fetch_result = await self._session.execute(stmt)
        results = fetch_result.scalars().all()
        return (
            [ProcessedAgentDataInDB.model_validate(result) for result in results]
            if results
            else None
        )

    async def getAll(self):
        stmt = select(self._model).order_by(self._model.id)
        result = await self._session.execute(stmt)
        results = result.scalars().all()
        return (
            [ProcessedAgentDataInDB.model_validate(result) for result in results]
            if results
            else None
        )
