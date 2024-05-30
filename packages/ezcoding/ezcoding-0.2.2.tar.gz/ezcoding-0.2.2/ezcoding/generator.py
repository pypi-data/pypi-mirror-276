# -*- coding: utf-8 -*-

import abc
from typing import AnyStr


class Generator(abc.ABC):

    @abc.abstractmethod
    def generate(self, *args, **kwargs) -> AnyStr:
        """Generate a string depending on the given arguments.

        Args:
            *args: position arguments
            **kwargs: keyword arguments

        Returns:
            A string representing the value of variable
        """
        pass
