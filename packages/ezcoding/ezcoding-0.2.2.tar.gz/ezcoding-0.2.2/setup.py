# coding: utf-8

from pathlib import Path
from configparser import ConfigParser

from setuptools import setup, find_packages


def load_readme() -> str:
    filename = Path.cwd().joinpath('README.md')
    if filename.is_file():
        with open(filename, 'r', encoding='utf-8') as fp:
            return fp.read()


def load_requires() -> list[str]:
    filename = Path.cwd().joinpath('Pipfile')
    if not filename.is_file():
        return []
    parser = ConfigParser()
    parser.read(filenames=filename, encoding='utf-8')
    return parser.options('packages')


setup(
    name='ezcoding',
    version='0.2.2',
    packages=find_packages(),
    url='https://gitee.com/zhuuuoyue/ezcoding',
    license='MIT',
    author='zhuoy',
    author_email='zhuoyue_cn@yeah.net',
    description='Easy coding',
    long_description=load_readme(),
    long_description_content_type='text/markdown',
    install_requires=load_requires(),
    entry_points={
        'console_scripts': [
            'ezc = ezcoding_cli.cli:main'
        ]
    }
)
