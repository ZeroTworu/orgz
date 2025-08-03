from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ActivityDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    activity_id: UUID = Field(..., alias='id')
    parent_id: UUID | None
    name: str


class ActivityTreeDto(ActivityDto):
    children: List['ActivityTreeDto']

