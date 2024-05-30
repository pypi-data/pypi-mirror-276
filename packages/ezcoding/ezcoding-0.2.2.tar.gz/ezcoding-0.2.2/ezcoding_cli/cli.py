# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from typing import Tuple, AnyStr, Union
from argparse import ArgumentParser

from ezcoding import Task


def parse_arguments() -> Tuple[Path, AnyStr]:
    parser = ArgumentParser()
    parser.add_argument('--filename', type=str, required=True)
    parser.add_argument('--template', type=str, required=True)
    values = parser.parse_args()
    return Path(values.filename), values.template


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


def main():
    template_dir = parse_template_dir()
    if template_dir is None:
        return
    filename, template_name = parse_arguments()
    task = Task(template_dir=template_dir, template_name=template_name)
    task.run(filename)


if __name__ == '__main__':
    main()
