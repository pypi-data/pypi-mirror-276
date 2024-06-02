# -*- coding: utf-8 -*-

import os.path
from pathlib import Path
from typing import Dict, AnyStr, Union, Optional, Sequence

from ezcoding.template import Template
from ezcoding.generator import Generator
from ezcoding.ui import Application, Editor
from ezcoding.const import FILENAME_KEY, TEMPLATE_KEY
from ezcoding.utils import create_variable_macro, load_module


class Task(object):

    def __init__(self, template_dir: Path, template_name: Optional[AnyStr] = None):
        self.__template_directory: Path = template_dir
        self.__template_name: Union[None, AnyStr] = template_name

    def list_templates(self) -> Sequence[AnyStr]:
        result: list[str] = list()
        it = self.__template_directory.iterdir()
        for item in it:
            if not item.is_file():
                continue
            stem, ext = os.path.splitext(item.name)
            if len(stem) == 0 or ext.lower() != '.py':
                continue
            result.append(stem)
        return result

    def run(self, filename: Path, values: Optional[Dict[AnyStr, AnyStr]] = None):
        template = self.__load_template()
        assert isinstance(template, Template)

        abs_filename = filename
        if not abs_filename.is_absolute():
            abs_filename = Path.cwd().joinpath(filename)
        value_dict = self.__create_values(abs_filename, template, values)

        text = template.complete(value_dict)
        self.__write_file(abs_filename, text)

    def __get_template_path(self) -> Path:
        return Path(self.__template_directory).joinpath(f'{self.__template_name}.py')

    def __load_template(self) -> Union[None, Template]:
        assert isinstance(self.__template_name, str)
        try:
            filename = self.__get_template_path()
            module = load_module(self.__template_name, filename)
            template = module.get_template()
            return template
        except AttributeError:
            return None

    def __create_values(self, filename: Path, template: Template, values: Optional[Dict[AnyStr, AnyStr]] = None) -> \
            Dict[AnyStr, AnyStr]:

        result = values if isinstance(values, dict) else dict()
        if FILENAME_KEY not in result:
            result[FILENAME_KEY] = str(filename.absolute())
        if TEMPLATE_KEY not in result:
            result[TEMPLATE_KEY] = str(self.__get_template_path())

        default_values = template.get_value_generators()
        for default_key in default_values:
            default_value = default_values[default_key]
            if default_key in result:
                continue
            if isinstance(default_value, Generator):
                result[default_key] = default_value.generate(**result)
            elif isinstance(default_value, str):
                result[default_key] = default_value

        variables = template.get_variables()
        will_edit_variables = False
        for variable in variables:
            if variable not in result:
                result[variable] = create_variable_macro(variable)
                will_edit_variables = True
        if will_edit_variables:
            Task.__edit_values(result)
        return result

    @staticmethod
    def __edit_values(values: Dict[AnyStr, AnyStr]):
        app = Application()
        dlg = Editor(values)
        dlg.show()
        app.exec()

    @staticmethod
    def __write_file(filename: Path, text: AnyStr):
        with open(filename, 'w') as fp:
            fp.write(text)
