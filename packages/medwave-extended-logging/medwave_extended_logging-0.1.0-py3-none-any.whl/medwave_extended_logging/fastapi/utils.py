"""Cusom logging utilities."""

import asyncio
import logging
from typing import List

from fastapi import FastAPI

from extended_sql import AsyncDBManager

from ..formatters import ConsoleFormatter
from ..utils import _safely_start_logger
from .handlers import TrafficDatabaseHandler
from .middlewares import LoggingMiddleware


async def setup_logger(
    name: str = None,
    level: str = "INFO",
    console_formatter: logging.Formatter = None,
    db_manager: AsyncDBManager = None,
    schema: str = "logs",
    console_: bool = True,
    database_: bool = True,
    drop_: bool = False,
    timeout: int = 99999,
    db_workers: int = 8,
) -> List[asyncio.Task]:
    """
    Set up and return a custom logger with the specified name and level.

    :param name: Name of the logger.
    :type name: str
    :param level: Logging level, e.g., 'INFO', 'DEBUG'.
    :type level: str
    :param console_formatter: Formatter instance to use for loging messages into console.
    :type console_formatter: logging.Formatter
    :param db_manager: AsyncDBManager to use for logging messages into database.
    :type db_manager: AsyncDBManager
    :param schema: The schema to use for the database table.
    :type schema: str
    :param console_: Whether to log to console (add console handler)
    :type console_: bool
    :param database_: Whether to log to database (add database handler)
    :type database_: bool
    :param drop_: Whether to drop the table before creating it.
    :type drop_: bool
    :param timeout: The timeout for the queue.
    :type timeout: int
    :param db_workers: The number of workers to use for the database handler.
    :type db_workers: int
    :return: Configured logger instance.
    :rtype: logging.Logger
    """
    if not console_ and not database_:
        raise ValueError("At least one of console_ or database_ must be True.")
    tasks = []

    # add console handler
    if console_:
        if console_formatter is None:
            console_formatter = ConsoleFormatter(name=name)

        console_handler = logging.StreamHandler()
        tasks.append(
            await _safely_start_logger(
                name=name + "_console",
                original_name=name,
                level=level,
                formatter=console_formatter,
                handler=console_handler,
                timeout=timeout,
            )
        )

    # add database handler
    if database_:
        db_handler = await TrafficDatabaseHandler.create(
            db_manager=db_manager,
            table_name=name,
            drop_=drop_,
            schema=schema,
            timeout=timeout,
            num_workers=db_workers,
        )

        tasks.append(
            await _safely_start_logger(
                name=name + "_database",
                original_name=name,
                level=level,
                handler=db_handler,
                timeout=timeout,
            )
        )

    return tasks


def register_middleware(app: FastAPI, logger_name: str) -> None:
    """
    Register the logging middleware to the FastAPI app.

    :param app: The FastAPI app instance.
    :type app: FastAPI
    :param logger_name: The name of the logger.
    :type logger_name: str
    """
    app.middleware("http")(
        LoggingMiddleware(
            logger_name=logger_name,
        )
    )
