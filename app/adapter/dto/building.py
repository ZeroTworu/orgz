from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BuildingDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    building_id: UUID = Field(..., alias='id')
    adress: str
