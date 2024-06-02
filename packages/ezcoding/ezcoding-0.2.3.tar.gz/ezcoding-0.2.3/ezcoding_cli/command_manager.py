# -*- coding: utf-8 -*-

from typing import Dict, AnyStr, Union, Self, Sequence

from ezcoding_cli.command import Command


_singleton = None


class CommandManager(object):

    @classmethod
    def get(cls) -> Self:
        global _singleton
        if _singleton is None:
            _singleton = CommandManager()
        return _singleton

    def __init__(self):
        self.__commands: Dict[AnyStr, Command] = dict()

    def add_command(self, command: Command) -> Self:
        if command.command_id not in self.__commands:
            self.__commands[command.command_id] = command
        return self

    def get_command(self, command_id: AnyStr) -> Union[None, Command]:
        return None if command_id not in self.__commands else self.__commands[command_id]

    def get_commands(self) -> Sequence[AnyStr]:
        return [cmd for cmd in self.__commands]
