import typing as _t
import sqlalchemy as _sa
import sqlalchemy.engine as _sae
import pathlib as _pl
from .util import file as _fu
from . import types as _types
from .util.db import (
    schema as _dbu_schema,
    seed as _dbu_seed,
    conn as _dbu_conn,
)


def create_schema(url: _sae.URL | str, schema: _types.SchemaDef):
    """Uses the schema definition to create the schema inside the passed database url"""
    match schema.type:
        case "sqlalchemy":
            _dbu_schema.load_sqlalchemy_schema(url, schema.value)
        case "file":
            with open(schema.value, "r") as f:
                fdata = f.read()
            _dbu_schema.load_sql_schema(url, fdata)
        case "raw_sql":
            _dbu_schema.load_sql_schema(url, schema.value)


def _seed_data_from_file(fname: str) -> _types.SeedData:
    fext = _pl.Path(fname).suffix.lower()
    match fext:
        case ".json":
            ftype = "json"
        case ".sql":
            ftype = "sql"
        case _:
            raise _types.ApiError(
                message=f"File type extension not recognized, must be `sql` or `json`: {fname}"
            ).to_httperr()
    with open(fname, "r") as f:
        fdata = f.read()

    return _types.SeedData(type=ftype, value=fdata)


def _seed_data_from_module(modname: str) -> _types.SeedData:
    try:
        fname = _fu.module_path(modname)
    except ValueError as e:
        raise _types.ApiError(message=str(e)).to_httperr()
    return _seed_data_from_file(fname)


def load_seed_data_list(
    url: _sae.URL | str,
    seeds: _t.List[_types.SeedData],
    *,
    reset_seq: bool,
    schema: _types.SchemaDef,
):
    if len(seeds) <= 0:
        return
    engine = _sae.create_engine(url)
    with _dbu_conn.disabled_constraints(engine) as conn:
        for seed in seeds:
            load_seed_data(conn, seed)
        if reset_seq:
            _reset_seq(conn, schema)


def load_seed_data(conn: _sae.Connection, seed: _types.SeedData):
    if seed.type == "file":
        seed = _seed_data_from_file(seed.value)
    if seed.type == "module":
        seed = _seed_data_from_module(seed.value)

    # at this point seed should have either a "json" or "sql" type
    match seed.type:
        case "json":
            _dbu_seed.load_json_seed(conn, seed.value)
        case "sql":
            _dbu_seed.load_sql_seed(conn, seed.value)


def _reset_seq(conn: _sae.Connection, schema: _types.SchemaDef):
    if schema.type != "sqlalchemy":
        # nothing to do
        return

    metadata = _fu.import_from_str(schema.value)
    if not metadata or not isinstance(metadata, _sa.MetaData):
        raise _types.ApiError(
            message=f"Not a valid metadata module: {schema.value}"
        ).to_httperr()

    _dbu_seed.reset_pg_seq(conn, metadata)
