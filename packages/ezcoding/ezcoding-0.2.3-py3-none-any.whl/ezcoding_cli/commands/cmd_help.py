# -*- coding: utf-8 -*-

from typing import Sequence, AnyStr, NoReturn

from ezcoding_cli.command import Command
from ezcoding_cli.command_manager import CommandManager


class CmdHelp(Command):

    def __init__(self):
        super().__init__(command_id='help', description='Show all commands.')

    def execute(self, argv: Sequence[AnyStr]) -> NoReturn:
        table: list[list[str]] = list()
        max_cmd_len: int = 0
        cmd_mgr = CommandManager.get()
        commands = cmd_mgr.get_commands()
        for command_id in commands:
            command = cmd_mgr.get_command(command_id)
            if command is None:
                continue
            table.append([command.command_id, command.description])
            if len(command.command_id) > max_cmd_len:
                max_cmd_len = len(command.command_id)

        print('ezc - Create file using defined template.')
        print('Usable subcommands:')

        for row in table:
            print(f'    {row[0].ljust(max_cmd_len)} - {row[1]}')


__all__ = ['CmdHelp']
