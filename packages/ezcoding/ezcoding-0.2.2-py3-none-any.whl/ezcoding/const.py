# -*- coding: utf-8 -*-

import re

FILENAME_KEY = '__filename'
TEMPLATE_KEY = '__template'

VARIABLE_PATTERN = re.compile(r'\$[_A-Za-z][_A-Za-z0-9]*\$')
