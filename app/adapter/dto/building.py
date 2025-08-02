from uuid import UUID
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, ConfigDict, Field, field_serializer

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from geoalchemy2.elements import WKBElement
    from geoalchemy2.elements import WKTElement


class BuildingDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    building_id: UUID = Field(..., alias='id')
    adress: str
    cords: object

    @field_serializer('cords')
    def serialize_cords(self, point: 'WKBElement|WKTElement') -> dict[str, float]:
        if point is None:
            return {'latitude': 0.0, 'longitude': 0.0}

        shape = to_shape(point)
        return {
            'longitude': shape.x,
            'latitude': shape.y,
        }

