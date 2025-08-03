from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.adapter.dto.activity import ActivityDto
from app.adapter.dto.building import BuildingDto


class PhoneDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    phone: str


class SimpleOrganizationDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    organization_id: UUID = Field(..., alias='id')
    name: str


class OrganizationDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    organization_id: UUID = Field(..., alias='id')
    name: str
    phones: List[str]
    activity: ActivityDto
    building: BuildingDto

    @classmethod
    def model_validate(cls, obj) -> 'OrganizationDto':
        return super().model_validate({
            **obj.__dict__,
            'phones': [phone.phone for phone in getattr(obj, 'phones', [])],
        })
