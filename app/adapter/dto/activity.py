from typing import List
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field


class ActivityDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    activity_id: UUID = Field(..., alias='id')
    name: str


class ActivityTreeDto(ActivityDto):
    children: List['ActivityTreeDto']


class NameQueryDto(BaseModel):
    name: str

def organization_name_query_dto(name: str = Query(...), ) -> NameQueryDto:
    return NameQueryDto(name=name)
