import uuid

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (Mapped, declarative_base, mapped_column,
                            relationship)

Base = declarative_base()


class BaseMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class Activity(Base, BaseMixin):
    __tablename__ = 'activity'

    name: Mapped[str] = mapped_column(String, nullable=False)

    lft: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    rgt: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey('activity.id', ondelete='SET NULL'), nullable=True
    )

    parent: Mapped['Activity'] = relationship(
        back_populates='children', remote_side='Activity.id'
    )

    children: Mapped[list['Activity']] = relationship(
        back_populates='parent', cascade='all'
    )

    organizations: Mapped['Organization'] = relationship(
        back_populates='activity', cascade='all'
    )

    def __repr__(self):
        return f'Activity<{self.name}>'


class Building(Base, BaseMixin):
    __tablename__ = 'building'

    adress: Mapped[str] = mapped_column(String, nullable=False)

    cords: Mapped['Geometry'] = mapped_column(Geometry('POINT', spatial_index=False), nullable=False)

    organizations: Mapped['Organization'] = relationship(
        back_populates='building', cascade='all'
    )

    def __repr__(self):
        return f'Building(adress{self.adress}, cords={self.cords})'


class Organization(Base, BaseMixin):
    __tablename__ = 'organization'

    name: Mapped[str] = mapped_column(String, nullable=False)

    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('activity.id', ondelete='CASCADE')
    )
    activity: Mapped[Activity] = relationship(
        back_populates='organizations', cascade='all'
    )

    building_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('building.id', ondelete='CASCADE')
    )
    building: Mapped[Building] = relationship(
        back_populates='organizations', cascade='all'
    )

    def __repr__(self) -> 'str':
        return f'<Organization({self.name})>'
