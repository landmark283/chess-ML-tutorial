# -*- coding: utf-8 -*-
"""board.py —— 棋盘：数据结构 + 最基础的操作

设计约定（全教程都遵守，请记牢）：

  1. 棋盘在内存里是**一维列表**，长度 9。
  2. 格子编号 0..8，按"从左到右、从上到下"数（行优先 / row-major）：

         0 | 1 | 2
        ---+---+---
         3 | 4 | 5
        ---+---+---
         6 | 7 | 8

     编号 5 的邻居是 8（正下方）和 2（右上），这看起来别扭，
     但等你写到 L07 的"四个方向扫描"时，一维编号会比二维省一半代码。
  3. 对外的坐标永远是 (row, col)，行列都从 0 开始，左上角是 (0, 0)。
     一维编号只活在内部，这样调用的人不用想编号。
  4. 已经下过的子不在棋盘上，而在 history 里。
     棋类 AI 里"悔棋 / 搜索回溯"用得极多，独立的落子历史是最省心的做法。
"""

from constants import EMPTY, X, O, SIZE, N_CELLS, SYMBOLS


# ----------------------------------------------------------------------
# 坐标转换
# ----------------------------------------------------------------------
def to_index(row, col):
    """(row, col) -> 0..8 的编号。"""
    return row * SIZE + col


def to_coord(index):
    """0..8 的编号 -> (row, col)。"""
    return divmod(index, SIZE)   # 一步同时拿到商和余数：商是行，余数是列


# ----------------------------------------------------------------------
# 棋盘
# ----------------------------------------------------------------------
class Board:
    """3x3 井字棋棋盘。

    用法：
        b = Board()
        b.push(4)          # 在正中间落子
        b.push(0)          # 在左上角落子
        print(b)           # 打印出来看
        b.pop()            # 悔棋
    """

    def __init__(self):
        # 这是本课最重要的两行！
        self.cells = [EMPTY] * N_CELLS   # 9 个空的格子
        self.history = []                # 落子历史，每个元素是 0..8 的编号，我们这里的落子历史没有包含是谁落子的信息。那么我们只能根据每人一步棋，并且'X'方先下的方式，计算出每一步落子是谁在落子。不支持一方跳过行棋，或者连下两步的情况。

    # ---- 基本查询 ----
    def __len__(self):
        return len(self.history)

    @property
    def current_player(self):
        """现在该谁下：第 0 手下 X，第 1 手下 O，第 2 手下 X……
        偶数手 -> X，奇数手 -> O。"""
        return X if len(self.history) % 2 == 0 else O

    def is_legal(self, index):
        """编号 index 这个格子现在能不能下？"""
        return 0 <= index < N_CELLS and self.cells[index] == EMPTY

    def legal_moves(self):
        """返回所有能下的格子编号，从小到大。"""
        return [i for i in range(N_CELLS) if self.cells[i] == EMPTY]

    # ---- 落子 / 悔棋 ----
    def push(self, index):
        """落一子，并把这步记进历史。非法走法直接报错（不要放过它）。"""
        if not self.is_legal(index):
            raise ValueError("非法走法：格子 %r 不能下（越界或已被占据）" % (index,))
        self.cells[index] = self.current_player
        self.history.append(index)

    def pop(self):
        """悔棋：撤销最后一手，返回被撤销的编号。"""
        if not self.history:
            raise ValueError("没有可撤销的走法")
        index = self.history.pop()
        self.cells[index] = EMPTY
        return index

    # ---- 显示 ----
    def __str__(self):
        # 棋盘 + 格子编号，方便你输坐标时对照
        rows = []
        for r in range(SIZE):
            line = " ".join(SYMBOLS[self.cells[to_index(r, c)]] for c in range(SIZE))
            rows.append("  " + line)
        board_text = "\n".join(rows)
        numbering = "编号对照：  0 1 2 / 3 4 5 / 6 7 8"
        return board_text + "\n" + numbering


# ----------------------------------------------------------------------
# 演示用：另一种表示法（二维）
# ----------------------------------------------------------------------
def as_2d(cells):
    """把一个一维棋盘拆成 3 行，返回 [[...], [...], [...]]。

    只用来给你看"一维和二维怎么互换"，正式代码里不用它。
    """
    return [list(cells[r * SIZE:(r + 1) * SIZE]) for r in range(SIZE)]


def from_2d(rows):
    """把 [[...], [...], [...]] 摊平成一维。"""
    return [value for row in rows for value in row]
