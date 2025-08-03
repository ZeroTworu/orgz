from enum import Enum

from fastapi import HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func
from starlette.status import HTTP_400_BAD_REQUEST

from app.adapter.store.models import Building


class GeoSearchMode(Enum):
    RADIUS = 'radius'
    BBOX = 'bbox'


class SearchType(Enum):
    ACTIVITY_NAME = 'activity_name'
    ORGANIZATION_NAME = 'organization_name'
    BUILDING_ADDRESS = 'building_address'


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


class SimpleSearchQueryDto(BaseModel):
    search_str: str


class SearchQueryDto(SimpleSearchQueryDto):
    search_type: SearchType = SearchType.ACTIVITY_NAME


def search_query_dto(
        search_str: str = Query(...),  # noqa: WPS404
        search_type: SearchType = Query(SearchType.ACTIVITY_NAME),  # noqa: WPS404
) -> SearchQueryDto:
    return SearchQueryDto(
        search_str=search_str,
        search_type=search_type,
    )

def simple_search_query_dto(
        search_str: str = Query(...),  # noqa: WPS404
) -> SimpleSearchQueryDto:
    return SearchQueryDto(
        search_str=search_str,
    )

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
