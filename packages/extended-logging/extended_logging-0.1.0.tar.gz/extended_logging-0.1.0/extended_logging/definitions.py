"""Custom logging handlers."""

import asyncio
import inspect
import logging
import os
from datetime import datetime

from extended_sql import AsyncDBManager


class DatabaseHandler(logging.Handler):
    """Custom logging handler to save records to a database."""

    SIG_KILL = "KILLME"

    def __init__(
        self,
        db_manager: AsyncDBManager,
        table_name: str,
        timeout: int = 5,
        num_workers: int = 8,
    ):
        super().__init__()

        self.db_manager = db_manager
        self.loop = asyncio.get_event_loop()
        self.name = f"{table_name}_db_handler_queue"
        self.timeout = timeout
        self.num_workers = num_workers

        self._queue = asyncio.Queue()
        self._logger = logging.getLogger("extended_logging")

    @classmethod
    async def _create(
        cls,
        db_manager: AsyncDBManager,
        table_creator: callable,
        table_name: str,
        schema: str = "logs",
        drop_: bool = False,
        timeout: int = 5,
        num_workers: int = 8,
    ):
        """
        Create a new instance of the DatabaseHandler.

        :param db_manager: The database manager.
        :type db_manager: AsyncDBManager
        :param table_creator: The function to create the table. Will be fed with `table_name` and `schema`.
        :type table_creator: callable
        :param table_name: The name of the table to log to.
        :type table_name: str
        :param schema: The schema to use for the database table.
        :type schema: str
        :param drop_: Whether to drop the table.
        :type drop_: bool
        :param timeout: The timeout for the queue.
        :type timeout: int
        :param num_workers: The number of workers to use.
        :type num_workers: int
        :return: The new instance of the DatabaseHandler.
        :rtype: DatabaseHandler
        """
        self = cls(
            db_manager=db_manager,
            table_name=table_name,
            timeout=timeout,
            num_workers=num_workers,
        )

        self._logger.debug(f"{self.name}: initializing table and schemas")
        self._table_class = table_creator(table_name=table_name, schema=schema)
        try:
            await self.db_manager.register_schema(schema=schema)
            await self.db_manager.initialize(drop_=drop_, model=self._table_class)
            await asyncio.sleep(0)
        except Exception as e:
            self._logger.error(f"error initializing table: {e}")

        self._logger.debug(f"{self.name}: initializing queue listener")
        self._tasks = []
        for i in range(num_workers):
            worker_name = f"{self.name}_worker_{i+1}"
            self._tasks.append(
                asyncio.create_task(self._process_queue(i + 1), name=worker_name)
            )

        return self

    async def _process_queue(self, worker_name: str):
        while True:
            record = await self._queue.get()
            self._logger.debug(f"got: {record}")

            if record == DatabaseHandler.SIG_KILL:
                self._logger.debug(f"received SIG_KILL")
                self._queue.task_done()
                break

            await self._write_to_db(record)
            self._queue.task_done()

    def emit(self, record):
        if record.pathname.strip().endswith(
            "/src/utils/logging/fastapi/middlewares.py"
        ):
            return

        func_name = DatabaseHandler.get_func_name()
        if func_name is not None:
            record.funcName = func_name

        try:
            t = asyncio.run_coroutine_threadsafe(self._queue.put(record), self.loop)
            t.result()
        except Exception as e:
            self._logger.error(f"error putting record to queue: {e}")

        self._logger.debug(f"{self.name}: queue size: {self._queue.qsize()}")

    async def get_object(self, record) -> dict:
        """
        Called before writing to database, should return dict that will be passed to
        `table_class` constructor retrieved from `table_creator` callable.
        """
        raise NotImplementedError

    async def _write_to_db(self, record):
        try:
            await self.db_manager.insert(
                o=self._table_class(**await self.get_object(record=record))
            )
            self._logger.debug(f"saved: {record}")
        except Exception as e:
            self._logger.error(f"error saving record: {e}")

    async def shutdown(self):
        self._logger.debug(f"{self.name}: Attempting shutdown.")

        for _ in range(self.num_workers):
            await self._queue.put(DatabaseHandler.SIG_KILL)
        await self._queue.join()

        for task in self._tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                self._logger.debug(f"{self.name}: task {task.get_name()} cancelled.")

    @staticmethod
    def get_func_name() -> str:
        """
        Get the name of the function that called the logger.

        :return: The name of the function.
        :rtype: str
        """
        stack = inspect.stack()
        for frame in stack:
            if (
                not frame.function.startswith("_")
                and frame.function != "get_func_name"
                and frame.function not in ["emit", "format"]
                and "logging" not in frame.filename.split(os.sep)
            ):
                return frame.function

    @staticmethod
    def cut(o: str, length: int = 300) -> str:
        """
        Cut the string to the specified length if it is not None.

        :param o: The string to cut.
        :type o: str
        :param length: The length to cut to.
        :type length: int
        :return: The cut string.
        :rtype: str
        """
        return o[:length] if o is not None else None
