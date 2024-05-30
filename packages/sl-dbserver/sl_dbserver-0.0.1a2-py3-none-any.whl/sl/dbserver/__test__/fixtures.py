import pytest as _pytest
import typing as _t
import sqlalchemy as _sa
import sqlalchemy.engine as _sae
from .db import models as _m
from .. import (
    app as _app,
    types as _types,
)


@_pytest.fixture(scope="function")
def sldb_test_schema() -> _sa.MetaData:
    return _m.metadata


@_pytest.fixture(scope="function")
def sldb_test_url(pytestconfig) -> str:
    """The test connection to use for this test run"""
    db_url = pytestconfig.getoption("--testdb")
    if db_url is None:
        db_url = pytestconfig.getini("testdb")
    return db_url


@_pytest.fixture(scope="function")
def sldb_test_schema_module() -> str:
    return "sl.dbserver.__test__.db.models:metadata"


@_pytest.fixture(scope="function")
def sldb_test_schema_def(sldb_test_schema_module) -> _types.SchemaDef:
    return _types.SchemaDef(type="sqlalchemy", value=sldb_test_schema_module)


@_pytest.fixture(scope="function")
def sldb_test_seed_data() -> _t.List[_types.SeedData]:
    return [
        _types.SeedData(type="module", value="sl.dbserver.__test__:seeds/test01.json")
    ]


@_pytest.fixture(scope="function")
def sldb_test_reset_seq() -> bool:
    return True


@_pytest.fixture(scope="function")
def sldb_url(
    sldb_test_url,
    sldb_test_schema_def,
    request,
    sldb_test_seed_data,
    sldb_test_reset_seq,
):
    """Creates, yields, and cleans up a testing database"""
    test_name = request.node.name
    response = _app.create_db(
        _types.CreateDbArgs(
            url=sldb_test_url,
            append_name=test_name,
            with_timestamp=True,
            schema=sldb_test_schema_def,
            seeds=sldb_test_seed_data,
            reset_seq=sldb_test_reset_seq,
        )
    )
    yield response.url
    _app.drop_db(_types.DropDbArgs(drop_id=response.drop_id))


@_pytest.fixture(scope="function")
def sldb_engine(sldb_url):
    engine = _sae.create_engine(sldb_url)
    yield engine
    engine.dispose()


@_pytest.fixture(scope="function")
def sldb_conn(sldb_engine):
    with sldb_engine.connect() as conn:
        yield conn
