# -*- coding: utf-8 -*-

from typing import AnyStr


def is_built_in_variable(variable: AnyStr) -> bool:
    return variable.startswith('__') if isinstance(variable, str) else False


def create_variable_macro(variable_name: AnyStr) -> AnyStr:
    return f'${variable_name}$'
