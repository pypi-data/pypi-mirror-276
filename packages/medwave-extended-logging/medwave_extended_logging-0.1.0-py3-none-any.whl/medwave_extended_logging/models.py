from datetime import datetime
from typing import Optional

from sqlalchemy import REAL, BigInteger, Column, Integer, SmallInteger, UnicodeText
from sqlmodel import Field

from extended_sql import register_class
from extended_sql.models import ExtendedSQLModel, IdMixin


class LogRecordBase:
    """
    Reference to class defined by :func:`create_log_record_class`.
    Just for type hinting.
    """


def create_log_record_class(table_name: str, schema: str = "logs") -> LogRecordBase:
    """
    Creates a LogRecord class with the given table name and schema.

    :param table_name: The name of the table.
    :type table_name: str
    :param schema: The name of the schema.
    :type schema: str
    :return: The LogRecord class that has table representation.
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
        "module": Field(nullable=False, max_length=100),
        "path_name": Field(default=None, max_length=300),
        "message": Field(nullable=False, max_length=300),
        "func_name": Field(nullable=False, max_length=100),
        "stack_info": Field(default=None, sa_column=Column(UnicodeText)),
        "exc_text": Field(default=None, max_length=300),
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
            "module": str,
            "path_name": Optional[str],
            "message": str,
            "func_name": str,
            "stack_info": Optional[str],
            "exc_text": Optional[str],
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
