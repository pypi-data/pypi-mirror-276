# -*- coding: utf-8 -*-

import abc
import re
from typing import AnyStr, Dict, Set, Union

from ezcoding.generator import Generator
from ezcoding.const import VARIABLE_PATTERN
from ezcoding.utils import create_variable_macro


class Template(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_text(self) -> AnyStr:
        """Get file content template text.

        Returns:
            A string representing file content template
        """
        pass

    def get_variables(self) -> Set[AnyStr]:
        """Get all variables in this template.

        Returns:
            A set of string representing all variables
        """
        text = self.get_text()
        matched = re.findall(VARIABLE_PATTERN, text)
        return {item[1: -1] for item in matched}

    def get_value_generators(self) -> Dict[AnyStr, Generator]:
        """Get all values and generators of variable in this template.

        Returns:
            A dictionary representing the relationship between variables and values/generators.
        """
        return dict()

    def complete(self, values: Dict[AnyStr, Union[AnyStr, Generator]]) -> AnyStr:
        """Complete this template using the given variable dictionary.

        Args:
            values: A dictionary representing variable values/generators

        Returns:
            A string representing the completed template text
        """
        text = self.get_text()
        variables = self.get_variables()
        for variable in variables:
            if variable not in values:
                continue
            value = ''
            if isinstance(values[variable], str):
                value = values[variable]
            elif isinstance(values[variable], Generator):
                value = values[variable].generate(**values)
            text = text.replace(create_variable_macro(variable), value)
        return text

    def update_values(self, values: Dict[AnyStr, Union[AnyStr, Generator]]):
        """Update default variable value dictionary using the given values.

        Args:
            values: A dictionary representing variable values/generators
        """
        default_values = self.get_value_generators()
        for default_key in default_values:
            default_value = default_values[default_key]
            if default_key not in values and isinstance(default_value, (str, Generator)):
                values[default_key] = default_value
