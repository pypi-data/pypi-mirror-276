from typing import Any

from pydantic import Field, PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOGS_POSTGRES_USER: str = Field(
        "postgres", env="LOGS_USER", description="Postgres user for logs database."
    )
    LOGS_POSTGRES_PASSWORD: str = Field(
        "mypgdbpass",
        env="LOGS_PASSWORD",
        description="Password for Postgres user for logs database.",
    )
    LOGS_POSTGRES_DB: str = Field(
        "logs", env="LOGS_DB", description="Postgres database name for logs."
    )
    LOGS_POSTGRES_HOST: str = Field(
        "localhost", env="LOGS_HOST", description="Host for Postgres logs database."
    )
    LOGS_POSTGRES_PORT: int = Field(
        5432, env="LOGS_PORT", description="Port for Postgres logs database."
    )
    LOGS_POSTGRES_POOL_SIZE: int = Field(
        8,
        env="LOGS_POOL_SIZE",
        description="Connection pool size for Postgres logs database.",
    )
    LOGS_POSTGRES_PRUNE: bool = Field(
        True,
        env="LOGS_PRUNE",
        description="Whether to prune logs in Postgres database.",
    )

    LOGS_SCHEMA: str = Field(
        "logs", env="LOGS_SCHEMA", description="Schema for logs in Postgres database."
    )
    LOGS_TIMEOUT: int = Field(
        999999, env="LOGS_TIMEOUT", description="Timeout setting for logs."
    )
    LOGS_WORKERS: int = Field(
        2, env="LOGS_WORKERS", description="Number of workers for logs."
    )
    TECH_LOGS_WORKERS: int = Field(
        2, env="TECH_LOGS_WORKERS", description="Number of technical workers for logs."
    )

    NETWORK_LOGGER_NAME: str = Field(
        "network",
        env="NETWORK_LOGGER_NAME",
        description="Logger name for network logs.",
    )
    APP_LOGGER_NAME: str = Field(
        "app", env="APP_LOGGER_NAME", description="Logger name for application logs."
    )

    LOG_LEVEL: str = Field(
        "INFO", env="LOG_LEVEL", description="Log level for application logs."
    )
    TECH_LOG_LEVEL: str = Field(
        "WARNING", env="TECH_LOG_LEVEL", description="Log level for technical logs."
    )

    ASYNC_LOGS_POSTGRES_URI: PostgresDsn = None

    class Config:
        case_sensitive = True
        env_file = ".env"

    @field_validator("ASYNC_LOGS_POSTGRES_URI", mode="before")
    @classmethod
    def assemble_log_db_connection(cls, v: str | None, info: FieldValidationInfo):
        return cls._assemble_db_connection(v, info, "LOGS_")

    @classmethod
    def _assemble_db_connection(
        cls, v: str | None, info: FieldValidationInfo, prefix: str
    ) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get(prefix + "POSTGRES_USER"),
            password=info.data.get(prefix + "POSTGRES_PASSWORD"),
            host=info.data.get(prefix + "POSTGRES_HOST"),
            port=info.data.get(prefix + "POSTGRES_PORT"),
            path=f"{info.data.get(prefix + 'POSTGRES_DB') or ''}",
        )
