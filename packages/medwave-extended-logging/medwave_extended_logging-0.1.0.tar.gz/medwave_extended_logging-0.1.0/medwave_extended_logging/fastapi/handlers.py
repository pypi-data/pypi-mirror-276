"""Custom logging handlers for logging fastapi traffic."""

from datetime import datetime

from ..definitions import DatabaseHandler
from .models import create_request_log_record_class


class TrafficDatabaseHandler(DatabaseHandler):
    """Custom logging handler to log traffic into database."""

    @classmethod
    async def create(
        cls,
        **kwargs,
    ):
        return await cls._create(
            table_creator=create_request_log_record_class, **kwargs
        )

    async def get_object(self, record) -> dict:
        return dict(
            created_at=datetime.fromtimestamp(record.created),
            created_relative=record.relativeCreated,
            level=record.levelno,
            line_number=record.lineno,
            process=record.process,
            process_name=record.processName[:100],
            thread=record.thread,
            thread_name=record.threadName[:100],
            task_name=record.taskName[:100],
            request_uri=record.request_uri[:350],
            request_protocol=record.request_protocol[:50],
            request_method=record.request_method[:10],
            request_path=record.request_path[:300],
            request_host=record.request_host[:50],
            request_size=record.request_size,
            request_content_type=record.request_content_type[:100],
            request_headers=record.request_headers,
            request_body=record.request_body,
            remote_host=record.remote_host[:100],
            response_status_code=record.response_status_code,
            response_size=record.response_size,
            response_headers=record.response_headers,
            response_body=record.response_body,
            duration=record.duration,
        )
