# -*- coding: utf-8 -*-

from pathlib import Path
from configparser import ConfigParser
from typing import AnyStr, Optional

from ezcoding.generator import Generator


class AuthorGenerator(Generator):

    def __init__(self, default_value: Optional[AnyStr] = None):
        self.__default_value: AnyStr = str()
        if isinstance(default_value, str):
            self.__default_value = default_value

    def generate(self, *args, **kwargs) -> AnyStr:
        git_config_file_path = Path.home().joinpath('.gitconfig')
        if git_config_file_path.is_file():
            config_parser = ConfigParser()
            config_parser.read(git_config_file_path, encoding='utf-8')
            if config_parser.has_section('user'):
                options = config_parser.options('user')
                if 'name' in options:
                    return config_parser.get('user', 'name')
        return self.__default_value
