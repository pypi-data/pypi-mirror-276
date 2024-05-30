# ezcoding

## 简介

利用模板，快速生成文本文件，帮助开发者快速写代码。

## 配置

先安装 Python，再安装 `ezcoding`。

```shell
pip install ezcoding
```

新建 `templates` 文件夹，用于存放模板文件。模板文件是一个 Python 脚本文件，继承 `Template` 类，再通过一个 `get_template` 函数返回其实例。

```python
# -*- coding: utf-8 -*-

from typing import AnyStr, Dict

from ezcoding import Template, Generator
from ezcoding.generators import HeaderMacroGenerator, AuthorGenerator, DateStringGenerator


class Header(Template):

    def __init__(self):
        super().__init__()

    def get_text(self) -> AnyStr:
        return """/*
 * author: $Author$
 * date: $Date$
 */

#ifndef $HeaderMacro$
#define $HeaderMacro$

namespace $Namespace$
{
}

#endif // $HeaderMacro$
"""

    def get_value_generators(self) -> Dict[AnyStr, Generator]:
        return {
            'HeaderMacro': HeaderMacroGenerator(prefix='DEMO'),
            'Author': AuthorGenerator(),
            'Date': DateStringGenerator()
        }


def get_template() -> Template:
    return Header()
```

在用户目录下，新建 `.ezcoding` 文件，按以下格式指定模板存放的目录。

```json
{
    "template_dir": "C:\\path\\to\\your\\template\\directory"
}
```

确保将 `ezc.exe` 所在目录添加到环境变量 `Path` 中，使得在任意目录下都可以访问到 `ezc` 命令。

## 使用

在希望新建文件的目录下，使用命令创建文件。以下命令使用 `Header` 模板，创建文件 `HelloWorld.h`。

```shell
ezc --filename HelloWorld.h --template Header
```
