# -*- coding: utf-8 -*-

from pathlib import Path
from argparse import ArgumentParser
from typing import Sequence, AnyStr, NoReturn, Dict

from ezcoding import Task

from ezcoding_cli.command import Command
from ezcoding_cli.utils import parse_template_dir


class Arguments(object):

    def __init__(self, filename: Path, template_name: AnyStr):
        self.filename: Path = filename
        self.template_name: AnyStr = template_name
        self.values: Dict[AnyStr, AnyStr] = dict()


class CmdCreate(Command):

    def __init__(self):
        super().__init__(command_id='create', description='Create file using template.')

    def execute(self, argv: Sequence[AnyStr]) -> NoReturn:
        template_dir = parse_template_dir()
        if template_dir is None:
            return
        args = self.parse_arguments(argv=argv)
        task = Task(template_dir=template_dir, template_name=args.template_name)
        task.run(filename=args.filename, values=args.values)

    @staticmethod
    def parse_arguments(argv: Sequence[AnyStr]) -> Arguments:
        parser = ArgumentParser()
        parser.add_argument('filename', type=str)
        parser.add_argument('template', type=str)
        parser.add_argument('variable_value_pairs', nargs='*')
        namespace = parser.parse_args(argv)

        args = Arguments(Path(namespace.filename), namespace.template)
        for variable_value_pair in namespace.variable_value_pairs:
            parts = variable_value_pair.split('=')
            if len(parts) != 2:
                continue
            variable = parts[0]
            if len(variable) == 0:
                continue
            args.values[variable] = parts[1]
        return args


__all__ = ['CmdCreate']
