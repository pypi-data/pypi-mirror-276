# -*- coding: utf-8 -*-

from uuid import uuid4
from typing import Optional, AnyStr, List

from ezcoding.generator import Generator


class HeaderMacroGenerator(Generator):

    def __init__(self, prefix: Optional[AnyStr] = None, suffix: Optional[AnyStr] = None):
        self.__prefix: AnyStr = str()
        self.__suffix: AnyStr = 'H_INCLUDED'

        if isinstance(prefix, str):
            self.__prefix = prefix
        if isinstance(suffix, str):
            self.__suffix = suffix

    def generate(self, *args, **kwargs) -> AnyStr:
        parts: List[AnyStr] = list()
        if len(self.__prefix) > 0:
            parts.append(self.__prefix)
        parts.append(str(uuid4()).upper().replace('-', '_'))
        if len(self.__suffix) > 0:
            parts.append(self.__suffix)
        separator = '_'
        return f'__{separator.join(parts)}__'
