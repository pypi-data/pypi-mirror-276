import typing as _t
import sqlalchemy_utils as _su
import sqlalchemy as _sa
import sqlalchemy.orm as _sao
import sqlalchemy.engine as _sae
import sqlalchemy.engine.base as _saeb
import contextlib as _cl
import logging as _logging

_log = _logging.getLogger(__name__)


def _disable_constraints(dialect: str, sqlFn: _t.Callable[[str], None]):
    """Given the dialect type and a function that can take SQL statements and execute them,
    will disable the check constraints for the given dialect type.
    """
    if dialect == "sqlite":
        sqlFn("PRAGMA ignore_check_constraints=OFF")
        sqlFn("PRAGMA foreign_keys=OFF")
    elif dialect == "postgresql":
        # Only works when constraints are configured to be deferrable
        # sqlFn('SET CONSTRAINTS ALL DEFERRED')
        # More dangerous (because constraints are straight up not checked) but ideal for
        # restoring files from backup
        sqlFn("SET session_replication_role = replica")


def _enable_constraints(dialect: str, sqlFn: _t.Callable[[str], None]):
    """Given the dialect type and a function that will run sql statements, re-enables the check
    constraints for the given dialect type
    """
    if dialect == "sqlite":
        sqlFn("PRAGMA ignore_check_constraints=ON")
        sqlFn("PRAGMA foreign_keys=ON")
    elif dialect == "postgresql":
        # Only works when constraints are configured to be deferrable
        # sqlFn('SET CONSTRAINTS ALL IMMEDIATE')
        sqlFn("SET session_replication_role = DEFAULT")


@_cl.contextmanager
def disabled_constraints(engine: _saeb.Engine):
    dialect = engine.dialect.name

    with engine.connect() as conn:

        def run_sql(arg: str):
            nonlocal conn
            conn.exec_driver_sql(arg)

        _disable_constraints(dialect, run_sql)
        yield conn
        _enable_constraints(dialect, run_sql)


def disable_session_constraints(session: _sao.Session):
    dialect = session.get_bind().dialect.name

    def run_sql(arg: str):
        nonlocal session
        session.execute(arg)

    _disable_constraints(dialect, run_sql)


def enable_session_constraints(session: _sao.Session):
    dialect = session.get_bind().dialect.name

    def run_sql(arg: str):
        nonlocal session
        session.execute(arg)

    _enable_constraints(dialect, run_sql)


def drop_database(conn_str: _sae.URL | str):
    """Uses the provided connection string to ensure that the database it points to does not
    exist.
    """
    if _su.database_exists(str(conn_str)):
        _su.drop_database(str(conn_str))


def create_database(conn_str: _sae.URL | str):
    """Uses the provided connection string to ensure that the database it points to exists.
    If the database already exists, then it will destroy and recreate it.
    """
    drop_database(conn_str)
    if not _su.database_exists(str(conn_str)):
        _su.create_database(str(conn_str))
