# -*- coding: utf-8 -*-

import importlib.util
from pathlib import Path
from typing import Dict, AnyStr, Union, Optional

from ezcoding.template import Template
from ezcoding.generator import Generator
from ezcoding.ui import Application, Editor
from ezcoding.const import FILENAME_KEY, TEMPLATE_KEY
from ezcoding.utils import create_variable_macro


class Task(object):

    def __init__(self, template_dir: Path, template_name: AnyStr):
        self.__template_directory: Path = template_dir
        self.__template_name: AnyStr = template_name

    def run(self, filename: Path, values: Optional[Dict[AnyStr, Union[AnyStr, Generator]]] = None):
        template = self.__load_template()
        assert isinstance(template, Template)

        abs_filename = filename
        if not abs_filename.is_absolute():
            abs_filename = Path.cwd().joinpath(filename)
        value_dict = self.__create_values(abs_filename, template, values)

        text = template.complete(value_dict)
        self.__write_file(filename, text)

    def __get_template_path(self) -> Path:
        return Path(self.__template_directory).joinpath(f'{self.__template_name}.py')

    def __load_template(self) -> Union[None, Template]:
        try:
            filename = self.__get_template_path()
            if not filename.is_file():
                return None
            spec = importlib.util.spec_from_file_location(self.__template_name, filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            template = module.get_template()
            return template
        except:
            return None

    def __create_values(
            self,
            filename: Path,
            template: Template,
            values: Optional[Dict[AnyStr, Union[AnyStr, Path, Generator]]] = None)\
            -> Dict[AnyStr, Union[AnyStr, Path, Generator]]:
        value_dict = values if isinstance(values, dict) else dict()
        if FILENAME_KEY not in value_dict:
            value_dict[FILENAME_KEY] = filename.absolute()
        if TEMPLATE_KEY not in value_dict:
            value_dict[TEMPLATE_KEY] = self.__get_template_path()
        template.update_values(value_dict)
        variables = template.get_variables()
        edit_variables = False
        for variable in variables:
            if variable not in value_dict:
                value_dict[variable] = create_variable_macro(variable)
                edit_variables = True
        if edit_variables:
            Task.__edit_values(value_dict)
        return value_dict

    @staticmethod
    def __edit_values(values: Dict[AnyStr, Union[AnyStr, Generator]]):
        app = Application()
        dlg = Editor(values)
        dlg.show()
        app.exec()

    @staticmethod
    def __write_file(filename: Path, text: AnyStr):
        with open(filename, 'w') as fp:
            fp.write(text)
