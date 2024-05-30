import sqlalchemy as _sa
import sqlalchemy.engine as _sae
import sqlalchemy.engine.base as _saeb
from . import serialize as _dbu_ser, conn as _dbu_conn, schema as _dbu_schema
from .. import file as _fu
import logging as _logging
from ... import types as _types

_log = _logging.getLogger(__name__)


def _yield_all_tables(metadata: _sa.MetaData):
    yield from metadata.tables.values()


def _yield_all_columns(table: _sa.Table):
    yield from table.c


def reset_pg_seq(conn: _saeb.Connection, metadata: _sa.MetaData):
    """When loading data with postgresql any auto-incrementing counters are not automatically
    accounted for, so this will go through every column in every table, check if it has a
    counter, and if it does, set the value of that counter to the maximum value currently held
    within that column.
    """
    for table in _yield_all_tables(metadata):
        for col in _yield_all_columns(table):
            # check for sequence
            seq_id = (
                conn.execute(
                    f"SELECT pg_get_serial_sequence('{table.name}', '{col.name}')"
                )
                .scalars()
                .one_or_none()
            )
            if not seq_id:
                # no sequence attached to this column
                continue
            # find the highest current value in that table column
            max_val = conn.execute(_sa.select(_sa.func.max(col))).scalars().one()
            if max_val is None:
                # no values exist in this column; no need to change any sequences
                continue
            _log.info(f"Updating sequence {seq_id}; setting to {max_val}")
            new_max = (
                conn.execute(f"SELECT setval('{seq_id}', '{max_val}')").scalars().one()
            )
            if new_max != max_val:
                # something went wrong
                _log.error(
                    f"Failure setting {seq_id}; tried to set to {max_val}, received {new_max}"
                )


def load_json_seed(conn: _sae.Connection, seed: str):
    parsed = _fu.str_to_json(seed)
    metadata_str = parsed.get("metadata")
    if not metadata_str:
        raise _types.ApiError(
            message="JSON Seed data does not specify metadata"
        ).to_httperr()
    metadata = _dbu_schema.metadata_from_str(metadata_str)
    data = parsed.get("data")
    if not data:
        raise _types.ApiError(
            message="JSON Seed data does not specify any seed data"
        ).to_httperr()

    _dbu_ser.deserialize_db(
        metadata,
        parsed,
        conn=conn,
    )


def load_sql_seed(conn: _sae.Connection, seed: str):
    conn.execute(seed)
