"""Definitions for Drydock database tables."""

from sqlalchemy.schema import Table, Column, Sequence
from sqlalchemy.types import Boolean, DateTime, String, Integer
from sqlalchemy.dialects import postgresql as pg


class ExtendTable(Table):
    def __new__(cls, metadata):
        self = super().__new__(cls, cls.__tablename__, metadata,
                               *cls.__schema__)
        return self


class Tasks(ExtendTable):
    """Table for persisting Tasks."""

    __tablename__ = 'tasks'

    __schema__ = [
        Column('task_id', pg.BYTEA(16), primary_key=True),
        Column('parent_task_id', pg.BYTEA(16)),
        Column('subtask_id_list', pg.ARRAY(pg.BYTEA(16))),
        Column('result_status', String(32)),
        Column('result_message', String(128)),
        Column('result_reason', String(128)),
        Column('result_error_count', Integer),
        Column('status', String(32)),
        Column('created', DateTime),
        Column('created_by', String(16)),
        Column('updated', DateTime),
        Column('design_ref', String(128)),
        Column('request_context', pg.JSON),
        Column('action', String(32)),
        Column('terminated', DateTime),
        Column('terminated_by', String(16))
    ]


class ResultMessage(ExtendTable):
    """Table for tracking result/status messages."""

    __tablename__ = 'result_message'

    __schema__ = [
        Column('sequence', Integer, primary_key=True),
        Column('task_id', pg.BYTEA(16)),
        Column('message', String(128)),
        Column('error', Boolean),
        Column('context', String(32)),
        Column('context_type', String(16)),
        Column('ts', DateTime),
        Column('extra', pg.JSON)
    ]


class ActiveInstance(ExtendTable):
    """Table to organize multiple orchestrator instances."""

    __tablename__ = 'active_instance'

    __schema__ = [
        Column('dummy_key', Integer, primary_key=True),
        Column('identity', pg.BYTEA(16)),
        Column('last_ping', DateTime),
    ]


class BuildData(ExtendTable):
    """Table persisting node build data."""

    __tablename__ = 'build_data'

    __schema__ = [
        Column('node_name', String(16), primary_key=True),
        Column('task_id', pg.BYTEA(16)),
        Column('message', String(128)),
    ]
