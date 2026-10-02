# -*- coding: utf-8 -*-
"""rules.py —— 规则引擎：谁赢了？平局了吗？

井字棋的全部规则就两条：
    1. 8 条连线里有一条被同一个人占满 -> 那个人赢（横、竖、斜都在这 8 条里）
    2. 棋盘满了还没人赢 -> 平局

规则代码有个特点：**它很短，但错了会毁掉后面一切**。
L02 的搜索如果搜出一个"赢",你要能相信它真的赢。
所以这个文件会被 test_rules.py 反复检查。
"""

from constants import EMPTY, X, O, LINES, N_CELLS
from board import Board

# 三种对局结果
X_WINS = "X 赢"
O_WINS = "O 赢"
DRAW = "平局"
ONGOING = "进行中"


# ----------------------------------------------------------------------
# 胜负判定
# ----------------------------------------------------------------------
def winner(cells):
    """返回 X、O 或 None（没人赢）。

    这就是本课的第一个"规则核心"。注意它只写了 8 条线，
    斜线是那 8 条里最容易漏的两条 —— 漏了它，你的 AI 会看不见对角线上的绝杀。
    """
    for a, b, c in LINES:
        v = cells[a]
        if v != EMPTY and v == cells[b] and v == cells[c]:
            return v
    return None


def is_full(cells):
    """棋盘下满了吗？"""
    return EMPTY not in cells


def game_status(board):
    """给一个 Board，返回 (状态, 赢家)。

    状态是 X_WINS / O_WINS / DRAW / ONGOING 之一；赢家是 X / O / None。
    """
    w = winner(board.cells)
    if w == X:
        return X_WINS, X
    if w == O:
        return O_WINS, O
    if is_full(board.cells):
        return DRAW, None
    return ONGOING, None


def is_over(board):
    """对局结束了吗（有赢家或平局）？"""
    return game_status(board)[0] != ONGOING


# ----------------------------------------------------------------------
# 棋形字符串 <-> 棋盘
# ----------------------------------------------------------------------
def parse(text):
    """把 'X.O / .X. / ..O' 这样的字符串变成棋盘（列表）。

    '.' 或 '·' = 空，'X'/'x' = X，'O'/'o'/'0' = O。
    空白可以随便加，方便你在纸上和代码里对得上。

    这个函数主要是给**测试**用的：写测试时，
    `parse("XXX/.../...")` 比 `[1,1,1,0,0,0,0,0,0]` 好读一万倍。
    """
    cells = []
    for ch in text:
        if ch in ".·":
            cells.append(EMPTY)
        elif ch in "Xx":
            cells.append(X)
        elif ch in "Oo0":
            cells.append(O)
        elif ch.isspace() or ch == "/":
            continue          # 分隔符，跳过
        else:
            raise ValueError("看不懂的字符：%r" % (ch,))
    if len(cells) != N_CELLS:
        raise ValueError("应该有 %d 个格子，实际读到 %d 个" % (N_CELLS, len(cells)))
    return cells


def board_from_text(text):
    """parse() 的兄弟版本：直接给你一个能落子的 Board。

    做法不是"重新下一遍"（那样会把格子重新填一遍），
    而是直接把格子填好，再按 X/O 的数量补出一个等长的 history
    —— history 的作用只是记 "已经下过几手"，`current_player` 靠它算。

    ⚠️ 注意由此而来的一个限制：这时 history 里是占位数字，不是你真正走过的格子，
    所以**别再对这个棋盘 push 到已经下过的位置上**。
    想接着下，用 `board.is_legal(i)` 先判断；
    本课的测试 `test_board_from_text_restores_current_player` 会提醒你这一点。
    """
    cells = parse(text)
    board = Board()
    board.cells = cells
    n_x = cells.count(X)
    n_o = cells.count(O)
    # 合法的井字棋局面：X 先下，所以 X 的数量要么等于 O，要么比 O 多 1
    if n_x == n_o:
        n_moves = n_x + n_o
    elif n_x == n_o + 1:
        n_moves = n_x + n_o
    else:
        raise ValueError("局面不合法：X 有 %d 个，O 有 %d 个" % (n_x, n_o))
    board.history = [0] * n_moves      # 具体是哪几格不重要，只用来数手数
    return board


def has_winner(cells):
    """语义更清楚的小别名：某些测试里 `has_winner(...)` 比 `winner(...) is not None` 好读。"""
    return winner(cells) is not None
