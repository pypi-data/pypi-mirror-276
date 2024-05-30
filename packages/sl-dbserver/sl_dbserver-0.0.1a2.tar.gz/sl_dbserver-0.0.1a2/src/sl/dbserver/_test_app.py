import typing as _t
import unittest as _ut
import sqlalchemy_utils as _su
import sqlalchemy as _sa
import sqlalchemy.engine as _sae
import pytest as _pytest
from . import app as _app
from . import types as _types
from .__test__.db import models as _m
from .util import file as _file

_TC = _ut.TestCase()


def test_create_drop_test_db(sldb_test_url, sldb_test_schema_module):
    response = _app.create_db(
        _types.CreateDbArgs(
            url=sldb_test_url,
            append_name="test append",
            with_timestamp=True,
            schema=_types.SchemaDef(type="sqlalchemy", value=sldb_test_schema_module),
            seeds=[
                _types.SeedData(
                    type="module", value="sl.dbserver.__test__:seeds/test01.json"
                )
            ],
            reset_seq=True,
        )
    )
    _TC.assertTrue(_su.database_exists(response.url))

    # check that the tables were created
    engine = _sae.create_engine(response.url)
    with engine.connect() as connection:
        all_users = connection.execute(_sa.select(_m.User)).all()
    _TC.assertEqual(
        all_users,
        [
            (1, "user1", "user1@email.com"),
            (2, "user2", "user2@email.com"),
        ],
    )
    engine.dispose()

    # destroy the database, afterwards
    _app.drop_db(_types.DropDbArgs(drop_id=response.drop_id))
    _TC.assertFalse(_su.database_exists(response.url))


def test_reset_seq(sldb_conn: _sae.Connection):
    user_seq = sldb_conn.exec_driver_sql("SELECT last_value FROM user_id_seq").one()
    _TC.assertEqual(user_seq, (2,))


class TestNoResetSeq:
    @_pytest.fixture(scope="function")
    def sldb_test_reset_seq(self):
        return False

    def test_no_reset_seq(self, sldb_conn: _sae.Connection):
        user_seq = sldb_conn.exec_driver_sql("SELECT last_value FROM user_id_seq").one()
        _TC.assertEqual(user_seq, (1,))


class TestSqlLoad:
    @_pytest.fixture(scope="function")
    def sldb_test_seed_data(self):
        return [
            _types.SeedData(
                type="module", value="sl.dbserver.__test__:seeds/test01.sql"
            ),
        ]

    def test_load_sql_seed(self, sldb_conn):
        all_users = sldb_conn.execute(_sa.select(_m.User)).all()
        _TC.assertEqual(
            all_users,
            [
                (1, "user1", "user1@email.com"),
                (2, "user2", "user2@email.com"),
            ],
        )


class TestSqlSchema:
    @_pytest.fixture(scope="function")
    def sldb_test_schema_def(self) -> _types.SchemaDef:
        path_to_schema = _file.module_path("sl.dbserver.__test__:schema.sql")
        return _types.SchemaDef(type="file", value=path_to_schema)

    def test_load_sql_schema(self, sldb_conn):
        all_users = sldb_conn.execute(_sa.select(_m.User)).all()
        _TC.assertEqual(
            all_users,
            [
                (1, "user1", "user1@email.com"),
                (2, "user2", "user2@email.com"),
            ],
        )


class TestRawSqlSchema:
    @_pytest.fixture(scope="function")
    def sldb_test_schema_def(self) -> _types.SchemaDef:
        path_to_schema = _file.module_path("sl.dbserver.__test__:schema.sql")
        with open(path_to_schema, "r") as f:
            raw_sql = f.read()
        return _types.SchemaDef(type="raw_sql", value=raw_sql)

    def test_load_sql_schema(self, sldb_conn):
        all_users = sldb_conn.execute(_sa.select(_m.User)).all()
        _TC.assertEqual(
            all_users,
            [
                (1, "user1", "user1@email.com"),
                (2, "user2", "user2@email.com"),
            ],
        )
