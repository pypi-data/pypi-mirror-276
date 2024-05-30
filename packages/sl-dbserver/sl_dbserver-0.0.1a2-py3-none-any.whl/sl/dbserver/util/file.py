import importlib.util as _ilu
import importlib as _il
import os
from os.path import exists
import json
from typing import Any


def module_path(path: str) -> str:
    """Takes in a path that can be either a regular path, a module, or a module followed by a path.
    They can take the form:

        <module>:<path>
        <module>
        <path>

    For example, if the module `sl.module` exists at `/home/user/proj/src/sl/module`, the following
    are example paths and what they would map to:

        # Regular absolute path
        > module_path('/home/user/proj/src/sl/module/subfolder/file.txt')
        '/home/user/proj/src/sl/module/subfolder/file.txt'

        # Module followed by a path
        > module_path('sl.module:subfolder/file.txt')
        '/home/user/proj/src/sl/module/subfolder/file.txt'

        # The path portion can start anywhere, even if it includes a "module" folder in it
        > module_path('sl:module/subfolder/file.txt')
        '/home/user/proj/src/sl/module/subfolder/file.txt'

        # Path directly to the module
        > module_path('sl.module')
        '/home/user/proj/src/sl/module'

        # Relative paths are unchanged
        > module_path('../some_file.txt')
        '../some_file.txt'

    It will not change paths that do not include the module component. If a path does not include
    the colon and has no slashes it will attempt to load the path as a module, and otherwise it
    will return the path unchanged.
    """
    if ":" in path:
        # If a colon does exist then we know for a fact that the lefthand side is meant to be a python module
        module, append = path.split(":")
        spec = _ilu.find_spec(module)
        if not spec or not spec.origin:
            raise ValueError(f"Module `{module}` does not appear to exist")
        dir_path = os.path.dirname(spec.origin)
        # Return the directory path plus the apended value
        return os.path.join(dir_path, os.path.normpath(append))
    # If there are no slashes and no colon, attempt to read the path as a module
    elif not ("/" in path or "\\" in path):
        spec = _ilu.find_spec(path)
        if not spec or not spec.origin:
            raise ValueError(f"Module `{path}` does not appear to exist")
        return os.path.dirname(spec.origin)

    # Otherwise this does not conform to anything we recognize; return the path unchanged
    return path


def import_from_str(module_name):
    """To import a module, just write it as you would a regular module:
        `my.module.path`
    To import a specific variable/function from the module, include the
    variable/function name after a colon:
        `my.module.path:var_name`
    """
    if ":" in module_name:
        module_str, var_str = module_name.split(":")
        module = _il.import_module(module_str)
        return module.__dict__[var_str]
    else:
        return _il.import_module(module_name)


def json_to_str(val: Any, *, sort_keys: bool = True, indent: int = 2) -> str:
    """Dumps to json string using default values. Primarily used for
    writing to files. `val` should already be json-serializable
    """
    return json.dumps(val, sort_keys=sort_keys, indent=indent)


def str_to_json(val: str) -> dict[Any, Any]:
    return json.loads(val)
