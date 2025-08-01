from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ActivityDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    activity_id: UUID = Field(..., alias='id')
    name: str


class BuildingDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    building_id: UUID = Field(..., alias='id')
    adress: str


class ActivityTreeDto(ActivityDto):
    children: List['ActivityTreeDto']


class OrganizationDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    organization_id: UUID = Field(..., alias='id')
    name: str
    activity_id: UUID
    building_id: UUID
