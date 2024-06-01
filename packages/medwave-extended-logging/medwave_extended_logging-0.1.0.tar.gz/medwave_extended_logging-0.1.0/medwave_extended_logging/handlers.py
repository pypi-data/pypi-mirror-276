from datetime import datetime

from .definitions import DatabaseHandler
from .models import create_log_record_class


class LoggingDatabaseHandler(DatabaseHandler):
    """Custom logging handler to log standard logging records to a database."""

    @classmethod
    async def create(
        cls,
        **kwargs,
    ):
        return await cls._create(table_creator=create_log_record_class, **kwargs)

    async def get_object(self, record) -> dict:
        return dict(
            created_at=datetime.fromtimestamp(record.created),
            created_relative=record.relativeCreated,
            level=record.levelno,
            line_number=record.lineno,
            process=record.process,
            process_name=DatabaseHandler.cut(record.processName, 100),
            thread=record.thread,
            thread_name=DatabaseHandler.cut(record.threadName, 100),
            task_name=DatabaseHandler.cut(record.taskName, 100),
            module=DatabaseHandler.cut(record.module, 100),
            path_name=DatabaseHandler.cut(record.pathname, 300),
            message=DatabaseHandler.cut(record.getMessage(), 300),
            func_name=DatabaseHandler.cut(record.funcName, 100),
            stack_info=record.stack_info,
            exc_text=DatabaseHandler.cut(record.exc_text, 300),
        )
