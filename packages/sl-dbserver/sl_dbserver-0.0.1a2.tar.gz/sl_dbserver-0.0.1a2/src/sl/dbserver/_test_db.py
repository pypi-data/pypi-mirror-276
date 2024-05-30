from unittest import TestCase as _TestCase
from . import db as _db

_TC = _TestCase()


def test_seed_data_from_module_json():
    loaded = _db._seed_data_from_module("sl.dbserver.__test__:seeds/test01.json")
    _TC.assertEqual(loaded.type, "json")


def test_seed_data_from_module_sql():
    loaded = _db._seed_data_from_module("sl.dbserver.__test__:seeds/test01.sql")
