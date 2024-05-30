import unittest as _ut

_TC = _ut.TestCase()


def test_json_to_str():
    from .file import json_to_str

    mydict = {
        "key": 12,
        "15": "value",
    }
    json_str = json_to_str(mydict)
    expected = '{\n  "15": "value",\n  "key": 12\n}'
    _TC.assertEqual(json_str, expected)


def test_str_to_json():
    from .file import str_to_json

    json_str = '{ "key": 8092, "otherkey": "value", "59": 20 }'
    expected = {
        "key": 8092,
        "otherkey": "value",
        "59": 20,
    }
    json_dict = str_to_json(json_str)
    _TC.assertEqual(json_dict, expected)
