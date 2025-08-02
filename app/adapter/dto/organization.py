from enum import Enum
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


class OrganizationDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    organization_id: UUID = Field(..., alias='id')
    name: str
    activity: ActivityDto
    building: BuildingDto


class OrganizationGeoQueryDto(BaseModel):
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
                return func.ST_DWithin(Building.cords, point, self.radius_meters)
            case GeoSearchMode.BBOX:
                envelope = func.ST_MakeEnvelope(
                    self.longitude - self.bbox_padding,
                    self.latitude - self.bbox_padding,
                    self.longitude + self.bbox_padding,
                    self.latitude + self.bbox_padding,
                    self.srid,
                )
                return func.ST_Within(Building.cords, envelope)
            case _:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Invalid mode. Use "radius" or "bbox".')


def organization_geo_query_dto(
        longitude: float = Query(...),
        latitude: float = Query(...),
        mode: GeoSearchMode = Query(GeoSearchMode.RADIUS),
        radius_meters: float = Query(1000),
        bbox_padding: float = Query(0.01),
        srid: int = Query(4326),
) -> OrganizationGeoQueryDto:
    return OrganizationGeoQueryDto(
        longitude=longitude,
        latitude=latitude,
        mode=mode,
        radius_meters=radius_meters,
        bbox_padding=bbox_padding,
        srid=srid,
    )
