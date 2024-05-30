import sqlalchemy as _sa
import sqlalchemy.engine as _sae
import typing as _t
from dateutil.parser import parse as _dateparse
import sqlalchemy.engine.base as _saeb
import sqlalchemy.orm as _sao
import sqlalchemy.types as _sat

import sqlalchemy as _sa

from .. import file as _fu

import logging as _logging

_log = _logging.getLogger(__name__)

SerializedTable = dict[str, _t.Any]


class SerializedDb(_t.TypedDict):
    """Type definition for a serialized data structure. The definition below leads to the basic
    structure:

    ```
    {
        "metadata": "path.to.module:metadata",
        "alembic": "<Alembic Revision>",
        "data": {
            "<table_name>": [
                {
                    "<column_name>": <value>,
                    ...
                },
                ...
            ],
            ...
        }
    }
    ```

    If `alembic` is not set, then the data cannot be tied to a specific
    revision of the database.
    """

    metadata: str
    # the alembic version number (if applicable)
    alembic: _t.Optional[str]
    # Actual table data. Takes the format of a dictionary of table names which map to lists of
    # objects which are dicts of column names to whatever SQLAlchemy data they contain.
    data: dict[str, list[SerializedTable]]


def _serialize_value(sql_type: _sat.TypeEngine, value: _t.Any) -> _t.Any:
    if hasattr(sql_type, "to_json"):
        return sql_type.to_json(value)
    elif isinstance(sql_type, _sa.DateTime):
        if value is not None:
            return value.isoformat()
        return value
    elif isinstance(sql_type, _sa.Enum):
        if value is not None:
            return value.name
        return value
    else:
        return value


def _deserialize_value(sql_type: _sat.TypeEngine, value: _t.Any) -> _t.Any:
    if hasattr(sql_type, "from_json"):
        return sql_type.from_json(value)
    elif isinstance(sql_type, _sa.DateTime):
        if value is not None:
            return _dateparse(value)
        return value
    else:
        return value


def serialize_db(
    metadata: _sa.MetaData, *, conn: _sao.Session, metadata_str: str
) -> SerializedDb:
    model_dict = dict()
    for t_name, t in metadata.tables.items():
        q = conn.query(t)
        all_rows = q.all()
        count_rows = q.count()
        _log.info(f"Dumping {count_rows} from table `{t_name}` ...")
        model_dict[t_name] = [
            {
                col.name: _serialize_value(col.type, val)
                for val, col in zip(r, t.columns.values())
            }
            for r in all_rows
        ]

    data_dict = {
        "metadata": metadata_str,
        "alembic": None,
        "data": model_dict,
    }

    return data_dict


def deserialize_db(
    metadata: _sa.MetaData,
    seed_dict: SerializedDb,
    *,
    conn: _sae.Connection,
) -> None:
    """Loads a model dictionary into the database."""
    model_dict = seed_dict["data"]
    for t_name in model_dict.keys():
        t = metadata.tables[t_name]
        _log.info(f"Loading {len(model_dict[t_name])} rows into table `{t_name}` ...")
        if len(model_dict[t_name]) <= 0:
            continue  # skip empty tables; sometimes trying to load them acts strangely
        rows = [
            {
                col_name: _deserialize_value(t.columns[col_name].type, val)
                for col_name, val in r.items()
            }
            for r in model_dict[t_name]
        ]
        conn.execute(t.insert(), [r for r in rows if len(r) > 0])
