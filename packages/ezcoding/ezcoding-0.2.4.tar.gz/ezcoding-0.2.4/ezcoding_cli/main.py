# -*- coding: utf-8 -*-

import sys
from typing import AnyStr, Tuple, Sequence

import ezcoding_cli.commands  # to load add commands
from ezcoding_cli.command_manager import CommandManager


def retrieve_command_and_arguments() -> Tuple[AnyStr, Sequence[AnyStr]]:
    if len(sys.argv) > 2:
        return sys.argv[1], sys.argv[2:]
    if len(sys.argv) >= 2:
        return sys.argv[1], list()
    return 'help', list()


def main():
    cmd_name, args = retrieve_command_and_arguments()
    cmd_mgr = CommandManager.get()
    cmd = cmd_mgr.get_command(command_id=cmd_name)
    if cmd is not None:
        cmd.execute(args)


if __name__ == '__main__':
    main()
