# -*- coding: utf-8 -*-

from typing import Sequence, AnyStr, NoReturn

from ezcoding import Task

from ezcoding_cli.command import Command
from ezcoding_cli.utils import parse_template_dir


class CmdListTemplates(Command):

    def __init__(self):
        super().__init__(command_id='list', description='List all usable templates.')

    def execute(self, argv: Sequence[AnyStr]) -> NoReturn:
        template_dir = parse_template_dir()
        if template_dir is None:
            return
        template_names = Task(template_dir=template_dir).list_templates()
        print('Template directory:')
        print(f'    - {template_dir}')
        print('Usable Templates:')
        for template_name in template_names:
            print(f'    - {template_name}')


__all__ = ['CmdListTemplates']
