# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Sequence, NoReturn, AnyStr, Optional


class Command(ABC):

    def __init__(self, command_id: AnyStr, description: Optional[AnyStr] = None):
        self.__command_id: AnyStr = command_id
        self.__description: AnyStr = str() if description is None else description

    @property
    def command_id(self) -> AnyStr:
        return self.__command_id

    @property
    def description(self) -> AnyStr:
        return self.__description

    @abstractmethod
    def execute(self, argv: Sequence[AnyStr]) -> NoReturn:
        pass
