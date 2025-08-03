from enum import Enum
from typing import List
from uuid import UUID

from fastapi import HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func
from starlette.status import HTTP_400_BAD_REQUEST

from app.adapter.dto.activity import ActivityDto
from app.adapter.dto.building import BuildingDto
from app.adapter.store.models import Building


class GeoSearchMode(Enum):
    RADIUS = 'radius'
    BBOX = 'bbox'

class PhoneDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    phone: str


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
            'phones': [p.phone for p in getattr(obj, 'phones', [])],
        })


class GeoQueryDto(BaseModel):
    longitude: float
    latitude: float
    mode: GeoSearchMode = GeoSearchMode.RADIUS
    radius_meters: float = 1000
    bbox_padding: float = 0.01,
    srid: int = 4326

    @property
    def condition(self):
        match self.mode:
            case GeoSearchMode.RADIUS:
                point = func.ST_SetSRID(func.ST_MakePoint(self.longitude, self.latitude), self.srid)
                return func.ST_DWithin(
                    func.Geography(Building.cords),
                    func.Geography(point),
                    self.radius_meters,
                )
            case GeoSearchMode.BBOX:
                envelope = func.ST_MakeEnvelope(
                    self.longitude - self.bbox_padding,
                    self.latitude - self.bbox_padding,
                    self.longitude + self.bbox_padding,
                    self.latitude + self.bbox_padding,
                    self.srid,
                )
                return func.ST_Within(
                    func.Geometry(Building.cords),
                    envelope,
                )
            case _:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Invalid mode. Use "radius" or "bbox".')


def geo_query_dto(
        longitude: float = Query(...),
        latitude: float = Query(...),
        mode: GeoSearchMode = Query(GeoSearchMode.RADIUS),
        radius_meters: float = Query(1000),
        bbox_padding: float = Query(0.01),
        srid: int = Query(4326),
) -> GeoQueryDto:
    return GeoQueryDto(
        longitude=longitude,
        latitude=latitude,
        mode=mode,
        radius_meters=radius_meters,
        bbox_padding=bbox_padding,
        srid=srid,
    )
