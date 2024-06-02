# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Union


def parse_template_dir() -> Union[Path, None]:
    config_file_path = Path.home().joinpath('.ezcoding')
    if not config_file_path.is_file():
        return None
    with open(config_file_path, 'r') as fp:
        data = json.load(fp)
    if 'template_dir' in data:
        template_dir = data['template_dir']
        template_dir_path = Path(template_dir)
        return template_dir_path if template_dir_path.is_dir() else None
    return None
