from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator, ConfigDict


class AccelerometerData(BaseModel):
    x: float
    y: float
    z: float


class GpsData(BaseModel):
    latitude: float
    longitude: float


class AgentData(BaseModel):
    accelerometer: AccelerometerData
    gps: GpsData
    timestamp: datetime

    @classmethod
    @field_validator("timestamp", mode="before")
    def check_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError(
                "Invalid timestamp format. Expected ISO 8601 format (YYYY - MM - DDTHH:MM: SSZ)."
            )

    def model_dump_flat(self):
        # Flatten the model by merging contact_info fields
        base = self.model_dump(exclude={"accelerometer", "gps"})
        accelerometer = self.accelerometer.model_dump()
        gps = self.gps.model_dump()
        return {**base, **accelerometer, **gps}


class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData

    def model_dump_flat(self):
        # Flatten the model by merging contact_info fields
        base = self.model_dump(exclude={"agent_data"})
        contact = self.agent_data.model_dump_flat()
        return {**base, **contact}


class ProcessedAgentDataInDB(BaseModel):
    id: Optional[int] = None
    road_state: str
    x: float
    y: float
    z: float
    latitude: float
    longitude: float
    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        json_encoders={Enum: lambda v: v.name.lower()},
    )
