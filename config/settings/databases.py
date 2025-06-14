from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBEngineEnum(StrEnum):
    SQLITE = "django.db.backends.sqlite3"
    POSTGRES = "django.db.backends.postgresql"


class BaseDatabaseSettings(BaseSettings):
    engine: DBEngineEnum
    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        extra="ignore",
        frozen=True,
        alias_generator=lambda field_name: field_name.upper(),
        populate_by_name=True,
        env_file=".env",
    )

    @field_validator("engine", mode="before")
    @classmethod
    def validate_engine(cls, v: Any) -> Any:
        """Allow both enum names and values for engine field."""
        valid_names = [member.name for member in DBEngineEnum]
        valid_values = [member.value for member in DBEngineEnum]
        if isinstance(v, str):
            try:
                return DBEngineEnum[v.upper()]
            except KeyError:
                pass

        for enum_member in DBEngineEnum:
            if v == enum_member.value:
                return enum_member

        raise PydanticCustomError(
            "enum",
            f"Input should be one of the enum names: {valid_names} "
            f"or one of the enum values: {valid_values}",
            {
                "input": v,
                "valid_names": valid_names,
                "valid_values": valid_values,
            },
        )


class SqliteDatabaseSettings(BaseDatabaseSettings):
    """Settings for SQLite database."""

    name: str = (
        Path(__file__).resolve().parent.parent.parent / "db.sqlite3"
    ).as_posix()


class PostgresDatabaseSettings(BaseDatabaseSettings):
    """Settings for PostgreSQL database."""

    port: int = 5432
    host: str = "localhost"
    password: str = "postgres"
    user: str = "postgres"
    name: str = "postgres"


class DjangoDatabases(BaseModel):
    """Django database settings."""

    default: PostgresDatabaseSettings | SqliteDatabaseSettings
