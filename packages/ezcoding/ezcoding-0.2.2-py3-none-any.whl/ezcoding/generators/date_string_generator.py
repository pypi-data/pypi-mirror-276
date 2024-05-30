# -*- coding: utf-8 -*-

from datetime import date
from typing import AnyStr

from ezcoding.generator import Generator


class DateStringGenerator(Generator):

    def generate(self, *args, **kwargs) -> AnyStr:
        return date.today().strftime('%Y-%m-%d')
