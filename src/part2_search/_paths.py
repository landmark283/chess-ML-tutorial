# -*- coding: utf-8 -*-
"""_paths.py —— 让 part2 能用到 part1 的棋盘和规则

为什么需要这个文件？

`board.py` / `rules.py` / `constants.py` 是**这个项目的地基**，
它们只该有一份（改一处、全项目生效）。所以 part2 不复制它们，而是
把 part1 的目录塞进 Python 的"模块搜索路径"里。

这就是 K1.1 讲过的 sys.path：Python 找模块时，就在这份名单里逐个目录找。
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
PART1 = os.path.join(SRC, "part1_tictactoe")

if PART1 not in sys.path:
    sys.path.insert(0, PART1)      # 放在最前面，优先从这里找

# 也把 part2 自己放进去，这样 part2 内部的模块能互相 import
if HERE not in sys.path:
    sys.path.insert(0, HERE)
