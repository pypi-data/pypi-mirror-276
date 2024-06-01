from pydantic import Field, PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from .config import Settings as BaseFastAPISettings


class Settings(BaseFastAPISettings):
    BACKEND_POSTGRES_USER: str = Field(
        "postgres",
        env="BACKEND_USER",
        description="Postgres user for backend database.",
    )
    BACKEND_POSTGRES_PASSWORD: str = Field(
        "mypgdbpass",
        env="BACKEND_PASSWORD",
        description="Password for Postgres user for backend database.",
    )
    BACKEND_POSTGRES_DB: str = Field(
        "backend", env="BACKEND_DB", description="Postgres database name for backend."
    )
    BACKEND_POSTGRES_HOST: str = Field(
        "localhost",
        env="BACKEND_HOST",
        description="Host for Postgres backend database.",
    )
    BACKEND_POSTGRES_PORT: int = Field(
        5432, env="BACKEND_PORT", description="Port for Postgres backend database."
    )
    BACKEND_POSTGRES_ECHO: bool = Field(
        False,
        env="BACKEND_ECHO",
        description="Whether to echo SQL statements for backend Postgres database.",
    )
    BACKEND_POSTGRES_POOL_SIZE: int = Field(
        8,
        env="BACKEND_POOL_SIZE",
        description="Connection pool size for Postgres backend database.",
    )
    ASYNC_BACKEND_POSTGRES_URI: PostgresDsn = None

    class Config:
        case_sensitive = True
        env_file = ".env"

    @field_validator("ASYNC_BACKEND_POSTGRES_URI", mode="before")
    @classmethod
    def assemble_backend_db_connection(cls, v: str | None, info: FieldValidationInfo):
        return cls._assemble_db_connection(v, info, "BACKEND_")
