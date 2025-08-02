from typing import TYPE_CHECKING, Any
from uuid import UUID

from geoalchemy2 import shape
from pydantic import BaseModel, ConfigDict, Field, field_serializer

if TYPE_CHECKING:
    from geoalchemy2.elements import WKBElement, WKTElement


class BuildingDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    building_id: UUID = Field(..., alias='id')
    adress: str
    cords: Any

    @field_serializer('cords')
    def serialize_cords(self, point: 'WKBElement|WKTElement') -> dict[str, float]:
        if point is None:
            return {'latitude': 0.0, 'longitude': 0.0}  # noqa: WPS358

        sh = shape.to_shape(point)
        return {
            'longitude': sh.x,
            'latitude': sh.y,
        }

