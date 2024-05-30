import sqlalchemy as _sa
import sqlalchemy.engine as _sae
from .. import file as _fu
from ... import types as _types


def load_sqlalchemy_schema(url: _sae.URL | str, value: str):
    metadata = _fu.import_from_str(value)
    if not isinstance(metadata, _sa.MetaData):
        raise _types.ApiError(
            message=f"Not a valid sqlalchemy metadata object: {value}"
        ).to_httperr()
    engine = _sae.create_engine(url)
    metadata.create_all(engine)


def load_sql_schema(url: _sae.URL | str, value: str):
    engine = _sae.create_engine(url)
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(value)


def metadata_from_str(metadata_str: str) -> _sa.MetaData:
    metadata = _fu.import_from_str(metadata_str)
    if not isinstance(metadata, _sa.MetaData):
        raise _types.ApiError(
            message=f"Not a valid metadata module: {metadata_str}"
        ).to_httperr()
    return metadata
