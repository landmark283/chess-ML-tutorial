# -*- coding: utf-8 -*-
"""buggy.py —— 🚪 出关测验用的"有病的棋盘"

这个文件里有 **3 个 bug**，每个都和 L01 的某个知识点有关。
它们都不会让程序崩溃 —— 这才是最可怕的地方：
程序照常跑，结果悄悄错掉。

你的任务（不是读代码猜，而是**写测试把它们钉死**）：
    1. 只用行为去撞它：写下"我期望什么"，看它给了什么
    2. 记录每个 bug：期望 / 实际 / 我用了哪条 assert 抓到它
    3. 改掉 buggy.py 里的 3 处代码，让你写的测试全绿

三个 bug 分别住在：
    · 数据表示 —— 初始化棋盘的那一行附近
    · 走法合法性 —— is_legal() 里
    · 规则判定 —— winner() 里

感觉无从下手的时候，用这个笨办法（但极其有效）：
**把"正确应该是什么"写成 assert，然后一条一条往 buggy.py 上撞。**
差异会自己跳出来。

顺便说一句：这个文件是**故意**写得和 board.py / rules.py 不一样的 ——
它用二维列表、用 dict 存游戏状态、用 (row, col) 下棋。
读别人的代码、并且能判断它对不对，本身就是一项要练的能力。
"""

import sys

sys.stdout.reconfigure(encoding="utf-8") # pyright: ignore[reportAttributeAccessIssue]

EMPTY, X, O = 0, 1, 2
SYMBOLS = ["·", "X", "O"]
SIZE = 3

# 8 条连线
LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def new_game():
    # ↓↓↓ bug ① 在这附近（想想 [[0]*3]*3 的后果）
    game = {
        "board": [[EMPTY] * SIZE] * SIZE,
        "history": [],
    }
    return game


def flat(board):
    """把 3x3 摊平成 9 个格子的列表。"""
    return [v for row in board for v in row]


def is_legal(game, row, col):
    """(row, col) 这一格能不能落子？"""
    cells = flat(game["board"])
    index = row * SIZE + col
    # ↓↓↓ bug ② 在这一行
    if cells[index] >= EMPTY:
        return True
    return False


def push(game, row, col):
    """在 (row, col) 落一子。"""
    if not is_legal(game, row, col):
        raise ValueError("非法走法 (%r, %r)" % (row, col))
    player = X if len(game["history"]) % 2 == 0 else O
    game["board"][row][col] = player
    game["history"].append((row, col))


def pop(game):
    """悔棋：撤销最后一手。"""
    if not game["history"]:
        raise ValueError("没有可撤销的走法")
    row, col = game["history"].pop()
    game["board"][row][col] = EMPTY


def winner(board):
    cells = flat(board)
    for a, b, c in LINES:
        v = cells[a]
        # ↓↓↓ bug ③ 在这一行
        if v == cells[b] and v == cells[c]:
            return v
    return None


def is_full(board):
    return all(v != EMPTY for v in flat(board))


def turn(game):
    return "X" if len(game["history"]) % 2 == 0 else "O"


def show(board):
    for row in board:
        print("  " + " ".join(SYMBOLS[v] for v in row))
    print("  坐标：(行, 列)，左上角是 (0, 0)")


def main():
    game = new_game()
    print("这是 buggy.py —— 有 3 处 bug 的井字棋。")
    print("先别急着改。先用它下几局，再用测试把它钉死。\n")
    while True:
        board = game["board"]
        show(board)
        w = winner(board)
        if w is not None:
            print("有人赢了：%s" % SYMBOLS[w])
            return
        if is_full(board):
            print("棋盘满了，平局。")
            return
        raw = input("轮到 %s，输入 '行 列'（如 1 1）：" % turn(game)).strip()
        if raw in ("q", "quit"):
            return
        try:
            row, col = (int(x) for x in raw.replace(",", " ").split())
            push(game, row, col)
        except (ValueError, IndexError) as e:
            print("这一步不行：%s" % e)


if __name__ == "__main__":
    main()
