from typing import Union

from fastapi import FastAPI

from extended_logging import setup_logger
from extended_logging.fastapi import (
    register_middleware as register_fastapi_logging_middleware,
)
from extended_logging.fastapi import setup_logger as setup_fastapi_logger
from extended_sql import AsyncDBManager

from .backend_config import Settings as BackendSettings
from .config import Settings as LoggingSettings


def _create_log_engine(settings: LoggingSettings):
    return AsyncDBManager(
        uri=str(settings.ASYNC_LOGS_POSTGRES_URI),
        name="log_engine",
        pool_size=settings.LOGS_POSTGRES_POOL_SIZE,
    )


def _register_middleware(app: FastAPI, settings: LoggingSettings) -> None:
    register_fastapi_logging_middleware(
        app=app, logger_name=settings.NETWORK_LOGGER_NAME
    )


def setup_backend_engine(app: FastAPI, settings: BackendSettings) -> None:
    """
    Sets up the default logger for the application.

    For settings examples refer to :mod:`extended_fastapi.backend_config`.
    DB manager will be set as `app.back_db_manager`.

    :param app: The FastAPI application.
    :type app: FastAPI
    :param settings: The settings to use.
    :type settings: LoggingSettings
    """
    app.back_db_manager = AsyncDBManager(
        uri=str(settings.ASYNC_BACKEND_POSTGRES_URI),
        name="backend_engine",
        pool_size=settings.BACKEND_POSTGRES_POOL_SIZE,
    )


def setup_default_logger(app: FastAPI, settings: LoggingSettings) -> None:
    """
    Sets up the default logger for the application.

    For settings examples refer to :mod:`extended_fastapi.config`.
    DB manager will be set as `app.log_db_manager`.

    :param app: The FastAPI application.
    :type app: FastAPI
    :param settings: The settings to use.
    :type settings: LoggingSettings
    """
    app.log_db_manager = _create_log_engine(settings=settings)
    _register_middleware(app=app, settings=settings)


async def create_default_logger(
    db_manager: AsyncDBManager,
    settings: Union[LoggingSettings, BackendSettings],
) -> None:
    """
    Creates loggers for extended_sql and extended_logging without database support.
    Creates loggers for the application and network with database support.

    All loggers are created with the settings from the settings object. For examples
    refer to :mod:`extended_fastapi.config`. If `settings` is a `BackendSettings` object
    the loggers for backend engine will be created as well

    :param db_manager: The database manager.
    :type db_manager: AsyncDBManager
    :param settings: The settings to use.
    :type settings: Union[LoggingSettings, BackendSettings]
    """

    await setup_logger(
        name="extended_sql",
        level=settings.TECH_LOG_LEVEL,
        db_manager=db_manager,
        drop_=settings.LOGS_POSTGRES_PRUNE,
        timeout=settings.LOGS_TIMEOUT,
        schema=settings.LOGS_SCHEMA,
        db_workers=settings.TECH_LOGS_WORKERS,
        database_=False,
    )
    await setup_logger(
        name="extended_logging",
        level=settings.TECH_LOG_LEVEL,
        db_manager=db_manager,
        drop_=settings.LOGS_POSTGRES_PRUNE,
        timeout=settings.LOGS_TIMEOUT,
        schema=settings.LOGS_SCHEMA,
        db_workers=settings.TECH_LOGS_WORKERS,
        database_=False,
    )
    await setup_logger(
        name="sqlalchemy.engine.Engine.backend_engine",
        level=settings.TECH_LOG_LEVEL,
        db_manager=db_manager,
        drop_=settings.LOGS_POSTGRES_PRUNE,
        timeout=settings.LOGS_TIMEOUT,
        schema=settings.LOGS_SCHEMA,
        db_workers=settings.TECH_LOGS_WORKERS,
        database_=False,
    )

    if isinstance(settings, BackendSettings):
        await setup_logger(
            name="sqlalchemy.engine.Engine.log_engine",
            level=settings.TECH_LOG_LEVEL,
            db_manager=db_manager,
            drop_=settings.LOGS_POSTGRES_PRUNE,
            timeout=settings.LOGS_TIMEOUT,
            schema=settings.LOGS_SCHEMA,
            db_workers=settings.TECH_LOGS_WORKERS,
            database_=False,
        )

    await setup_logger(
        name=settings.APP_LOGGER_NAME,
        level=settings.LOG_LEVEL,
        db_manager=db_manager,
        drop_=settings.LOGS_POSTGRES_PRUNE,
        timeout=settings.LOGS_TIMEOUT,
        schema=settings.LOGS_SCHEMA,
        db_workers=settings.LOGS_WORKERS,
    )
    await setup_fastapi_logger(
        name=settings.NETWORK_LOGGER_NAME,
        level=settings.LOG_LEVEL,
        db_manager=db_manager,
        drop_=settings.LOGS_POSTGRES_PRUNE,
        timeout=settings.LOGS_TIMEOUT,
        schema=settings.LOGS_SCHEMA,
        db_workers=settings.LOGS_WORKERS,
    )
