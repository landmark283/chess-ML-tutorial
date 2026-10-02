# -*- coding: utf-8 -*-
"""main.py —— 命令行双人对下井字棋

用法：
    python main.py

输入 0..8 落子（编号见棋盘下方对照），输入 q 退出，输入 h 看帮助。
本课的目标就是你亲手用它下完一整局。
"""

import sys

from board import Board
from rules import game_status, X_WINS, O_WINS, DRAW

sys.stdout.reconfigure(encoding="utf-8")   # Windows 控制台中文编码

HELP = """
怎么下：
  · 棋盘下方有编号对照：0 1 2 / 3 4 5 / 6 7 8
  · 直接输入编号再回车，就在那一格落子
  · 输入 q 退出，输入 h 看这段帮助，输入 u 悔棋
  · X 先下
"""


def show(board):
    print()
    print(board)
    print()


def main():
    board = Board()
    print("=" * 40)
    print("井字棋 · 命令行双人对下")
    print("=" * 40)
    print(HELP)

    while True:
        status, _ = game_status(board)
        if status != "进行中":
            show(board)
            print("对局结束：%s" % status)
            break

        show(board)
        who = "X" if board.current_player == 1 else "O"
        raw = input("轮到 %s，请输入格子编号（0-8）：" % who).strip()

        if raw in ("q", "quit", "exit"):
            print("退出。")
            return
        if raw in ("h", "help", "?"):
            print(HELP)
            continue
        if raw in ("u", "undo"):
            try:
                undone = board.pop()
                print("已撤销格子 %d 上的一手。" % undone)
            except ValueError as e:
                print("撤不了：%s" % e)
            continue

        # ---- 输入校验：这一步很重要，用户会输进各种东西 ----
        try:
            index = int(raw)
        except ValueError:
            print("『%s』不是数字。请输入 0-8 之间的编号。" % raw)
            continue

        if not board.is_legal(index):
            print("格子 %d 不能下（已经被占了，或者超出 0-8）。再试一个。" % index)
            continue

        board.push(index)

    print("再玩一局就重新运行 `python main.py`。")


if __name__ == "__main__":
    main()
