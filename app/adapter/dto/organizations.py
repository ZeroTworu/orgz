from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class ActivityDto(BaseModel):
    activity_id: UUID = Field(..., alias='id')
    name: str


class ActivityTreeDto(ActivityDto):
    children: List['ActivityTreeDto']


class OrganizationDto(BaseModel):
    organization_name: str
    activity: ActivityDto
