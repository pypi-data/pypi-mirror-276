"""Usefull models definitions for SQLModel."""

from datetime import datetime
from typing import Set
from uuid import UUID

from sqlmodel import Field, SQLModel
from uuid_extensions import uuid7


class ExtendedSQLModel(SQLModel):
    """Extended SQLModel with some helper methods."""

    @classmethod
    def get_fields_names(cls, alias=False) -> Set[str]:
        return set(cls.schema(alias)["properties"].keys())


class IdMixin(SQLModel):
    """Mixin for models with UUID primary key."""

    id: UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )


class TimestampMixin(SQLModel):
    """Mixin for models with created_at and updated_at fields."""

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False,
    )


class CreatorMixin(SQLModel):
    """
    Mixin for models with created_by and updated_by fields.
    Any model that uses this mixin should register an event listener for update and insert
    that will set this fields automatically.
    """

    created_by: str = Field(nullable=False, max_length=20)
    updated_by: str = Field(nullable=False, max_length=20)
