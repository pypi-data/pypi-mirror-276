# -*- coding: utf-8 -*-

from uuid import uuid4
from typing import AnyStr

from ezcoding.generator import Generator


class UuidStringGenerator(Generator):

    def generate(self, *args, **kwargs) -> AnyStr:
        return str(uuid4()).upper()
