from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import JSON, REAL, BigInteger, Column, Integer, SmallInteger
from sqlmodel import Field

from extended_sql import register_class
from extended_sql.models import ExtendedSQLModel, IdMixin


class RequestLogRecordBase:
    """
    Reference to class defined by :func:`create_request_log_record_class`.
    Just for type hinting.
    """


def create_request_log_record_class(
    table_name: str, schema: str = "logs"
) -> RequestLogRecordBase:
    """
    Creates a RequestLogRecordBase class with the given table name and schema.

    :param table_name: The name of the table.
    :type table_name: str
    :param schema: The name of the schema.
    :type schema: str
    :return: The RequestLogRecordBase class that has table representation.
    :rtype: RequestLogRecordBase
    """
    attrs = {
        "created_at": Field(
            default_factory=datetime.utcnow, nullable=False, index=True
        ),
        "created_relative": Field(sa_column=Column(REAL, nullable=False)),
        "level": Field(sa_column=Column(SmallInteger, nullable=False, index=True)),
        "line_number": Field(sa_column=Column(SmallInteger, nullable=False)),
        "process": Field(sa_column=Column(Integer, nullable=False, index=True)),
        "process_name": Field(default=None, max_length=100),
        "thread": Field(sa_column=Column(BigInteger, nullable=False)),
        "thread_name": Field(default=None, max_length=100),
        "task_name": Field(default=None, max_length=100),
        "request_uri": Field(nullable=False, max_length=350),
        "request_protocol": Field(nullable=False, max_length=50),
        "request_method": Field(nullable=False, max_length=10),
        "request_path": Field(nullable=False, max_length=300),
        "request_host": Field(nullable=False, max_length=50),
        "request_size": Field(sa_column=Column(Integer, nullable=False)),
        "request_content_type": Field(nullable=False, max_length=100),
        "request_headers": Field(sa_column=Column(JSON, nullable=False)),
        "request_body": Field(sa_column=Column(JSON, nullable=False)),
        "remote_host": Field(nullable=False, max_length=100),
        "response_status_code": Field(sa_column=Column(SmallInteger, nullable=False)),
        "response_size": Field(sa_column=Column(Integer, nullable=False)),
        "response_headers": Field(sa_column=Column(JSON, nullable=False)),
        "response_body": Field(sa_column=Column(JSON, nullable=False)),
        "duration": Field(sa_column=Column(SmallInteger, nullable=False)),
        "__annotations__": {
            "created_at": datetime,
            "created_relative": float,
            "level": int,
            "line_number": int,
            "process": int,
            "process_name": Optional[str],
            "thread": int,
            "thread_name": Optional[str],
            "task_name": Optional[str],
            "request_uri": str,
            "request_protocol": str,
            "request_method": str,
            "request_path": str,
            "request_host": str,
            "request_size": int,
            "request_content_type": str,
            "request_headers": Dict[str, Any],
            "request_body": Dict[str, Any],
            "remote_host": str,
            "response_status_code": int,
            "response_size": int,
            "response_headers": Dict[str, Any],
            "response_body": Dict[str, Any],
            "duration": int,
        },
    }
    return register_class(
        attrs=attrs,
        table_name=table_name,
        schema=schema,
        bases=(
            IdMixin,
            ExtendedSQLModel,
        ),
    )
