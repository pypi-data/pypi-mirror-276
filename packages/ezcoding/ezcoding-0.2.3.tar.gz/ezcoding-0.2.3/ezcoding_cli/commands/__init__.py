# -*- coding: utf-8 -*-

import os
from pathlib import Path

from ezcoding.utils import load_module

from ezcoding_cli.command import Command
from ezcoding_cli.command_manager import CommandManager


_loaded = False

if not _loaded:
    cmd_mgr = CommandManager.get()
    it = Path(__file__).parent.iterdir()
    for module_path in it:
        if not module_path.is_file():
            continue
        filename = module_path.name.lower()
        stem, ext = os.path.splitext(filename)
        if ext != '.py':
            continue
        if stem.startswith('__') and stem.endswith('__'):
            continue
        module = load_module(stem, module_path)
        for cls in module.__all__:
            cmd = getattr(module, cls)()
            if isinstance(cmd, Command):
                cmd_mgr.add_command(cmd)
    _loaded = True
