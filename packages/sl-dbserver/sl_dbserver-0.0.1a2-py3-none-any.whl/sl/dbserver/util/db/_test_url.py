from unittest import TestCase as _TestCase
import datetime as _dt
from . import url as _dbu

_TC = _TestCase()

_use_timestamp = _dt.datetime.strptime(
    "2022-04-23 14:05:34",
    "%Y-%m-%d %H:%M:%S",
)


def test_make_db_name():
    created_name = _dbu.make_db_name(
        "my_database",
        append="My appended string",
        at_timestamp=_use_timestamp,
    )
    _TC.assertEqual(
        created_name,
        "20220423140534_my_database_my_appended_string",
    )


def test_make_db_name_long():
    created_name = _dbu.make_db_name(
        "my_database",
        append="My appended and very long test name string",
        at_timestamp=_use_timestamp,
    )
    _TC.assertEqual(
        created_name,
        "20220423140534_my_database_my_appended_and_very_long_tes5119",
    )

def test_make_db_name_long_2():
    created_name = _dbu.make_db_name(
        "my_database",
        append="My appended and very long test name string thing",
        at_timestamp=_use_timestamp,
    )
    _TC.assertEqual(
        created_name,
        "20220423140534_my_database_my_appended_and_very_long_tesbf3f",
    )

def test_make_db_name_no_timestamp():
    created_name = _dbu.make_db_name(
        "my_database",
        append="My appended string",
    )
    _TC.assertEqual(
        created_name,
        "my_database_my_appended_string",
    )


def test_make_db_name_no_append():
    created_name = _dbu.make_db_name(
        "my_database",
        at_timestamp=_use_timestamp,
    )
    _TC.assertEqual(
        created_name,
        "20220423140534_my_database",
    )


def test_make_db_name_no_extra():
    created_name = _dbu.make_db_name(
        "my_database",
    )
    _TC.assertEqual(
        created_name,
        "my_database",
    )
