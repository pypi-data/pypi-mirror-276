# -*- coding: utf-8 -*-

import importlib.util
from pathlib import Path
from typing import AnyStr


def is_built_in_variable(variable: AnyStr) -> bool:
    return variable.startswith('__') if isinstance(variable, str) else False


def create_variable_macro(variable_name: AnyStr) -> AnyStr:
    return f'${variable_name}$'


def load_module(name: AnyStr, location: Path):
    if not location.is_file():
        return None
    spec = importlib.util.spec_from_file_location(name, location)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
