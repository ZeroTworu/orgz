from enum import Enum

from pydantic import BaseModel


class EsSearchType(Enum):
    ACTIVITY = 'activity'
    ORGANIZATION = 'organization'


class ElasticQueryDto(BaseModel):
    name: str
    type: EsSearchType = EsSearchType.ACTIVITY
