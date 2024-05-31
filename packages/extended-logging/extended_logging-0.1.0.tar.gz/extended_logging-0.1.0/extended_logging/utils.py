"""Cusom logging utilities."""

import asyncio
import logging
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from typing import List

from sqlalchemy.ext.asyncio import AsyncEngine

from extended_sql import AsyncDBManager

from .definitions import DatabaseHandler
from .formatters import ConsoleFormatter
from .handlers import LoggingDatabaseHandler

_logger = logging.getLogger("extended_logging")


class _SpecialHandler(logging.Handler):

    def __init__(self, log_event) -> None:
        super().__init__()
        self.log_event = log_event
        self.loop = asyncio.get_event_loop()

    def emit(self, record) -> None:
        t = asyncio.run_coroutine_threadsafe(self._alive(), self.loop)
        # t.result()

    async def _alive(self):
        self.log_event.set()


async def _logger_monitor(
    logger: logging.Logger, name: str, handler: logging.Handler, timeout: int = 5
):
    """
    Monitor the logger for a specified timeout period.
    """
    log_event = asyncio.Event()
    handle = _SpecialHandler(log_event)
    logger.addHandler(handle)

    try:
        while True:
            try:
                await asyncio.wait_for(log_event.wait(), timeout=timeout)
                log_event.clear()
            except asyncio.TimeoutError:
                if isinstance(handler, DatabaseHandler):
                    if not handler._queue.empty():
                        log_event.set()
                        _logger.warning(
                            f"No logs appeared within the timeout period ({timeout}). Yet it has a DataBase handler with queue of size {handler._queue.qsize()}."
                        )
                    else:
                        _logger.warning(
                            f"No logs appeared within the timeout period ({timeout}). Stopping logger."
                        )
                        await handler.shutdown()
                        _logger.warning(f"Logger {name} - stopped")
                        break
                else:
                    _logger.warning(
                        f"No logs appeared within the timeout period ({timeout}). Stopping logger."
                    )
                    break

    finally:
        logger.removeHandler(handle)


async def _init_logger(
    name: str,
    original_name: str,
    level: str = "INFO",
    formatter: logging.Formatter = None,
    handler: logging.Handler = logging.StreamHandler(),
    timeout: int = 5,
) -> None:
    """
    Set up and return a custom logger with the specified name and level.

    :param name: The name of the logger to be logged to as started.
    :type name: str
    :param original_name: The name of the logger.
    :type original_name: str
    :param level: The logging level.
    :type level: str
    :param formatter: The logging formatter.
    :type formatter: logging.Formatter
    :param handler: The logging handler.
    :type handler: logging.Handler
    :param timeout: The timeout for the queue.
    :type timeout: int
    """
    logger = logging.getLogger(original_name)
    logger.setLevel(level)

    if formatter is not None:
        handler.setFormatter(formatter)

    que = Queue()
    logger.addHandler(QueueHandler(que))
    listener = QueueListener(que, handler)

    try:
        listener.start()
        _logger.debug(f"Logger {name} has started ({level})")
        await _logger_monitor(
            logger=logger, name=name, timeout=timeout, handler=handler
        )
    except Exception as e:
        _logger.error(f"Logger {name} failed: {e}")
    finally:
        _logger.debug(f"Logger {name} is shutting down")
        listener.stop()


async def _safely_start_logger(name: str, **kwargs):
    """Safely start a logger."""
    _logger.debug(f"Attempting starting logger {name}")
    logger_task = asyncio.create_task(
        _init_logger(name=name, **kwargs), name=f"{name}_logger"
    )
    await asyncio.sleep(0)
    return logger_task


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
        db_handler = await LoggingDatabaseHandler.create(
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
