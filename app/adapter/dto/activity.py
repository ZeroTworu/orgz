from enum import Enum
from typing import List
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field


class SearchType(Enum):
    ACTIVITY_NAME = 'activity_name'
    ORGANIZATION_NAME = 'organization_name'
    BUILDING_ADDRESS = 'building_address'


class ActivityDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    activity_id: UUID = Field(..., alias='id')
    name: str


class ActivityTreeDto(ActivityDto):
    children: List['ActivityTreeDto']


class SimpleSearchQueryDto(BaseModel):
    search_str: str


def simple_search_query_dto(
        search_str: str = Query(...),  # noqa: WPS404
) -> SimpleSearchQueryDto:
    return SearchQueryDto(
        search_str=search_str,
    )


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
