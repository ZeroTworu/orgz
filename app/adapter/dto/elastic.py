from enum import Enum

from pydantic import BaseModel


class EsSearchType(Enum):
    ACTIVITY = 'activity'
    BUILDING = 'building'
    ORGANIZATION = 'organization'


class ElasticQueryDto(BaseModel):
    name: str
    type: EsSearchType = EsSearchType.ACTIVITY
