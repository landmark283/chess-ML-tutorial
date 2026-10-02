# -*- coding: utf-8 -*-
"""main.py —— 和你的 AI 下一局

用法：
    cd src/part2_search
    python main.py                 # 默认：完美 AI（搜到终局），你执 O 后手
    python main.py --first         # 你执 X 先手
    python main.py --depth 2       # 限深 2 层 + 手工评估的"弱化版" AI（你会赢！）
    python main.py --random        # 随机对手（你会赢得很轻松）

试试 `--depth 2` 和默认的差别 —— 这就是 K2.6 要讲的东西。
"""

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from _paths import PART1  # noqa: F401
sys.stdout.reconfigure(encoding="utf-8")

from board import Board
from rules import game_status


def parse_args(argv):
    opts = {"first": False, "depth": None, "random": False}
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--first":
            opts["first"] = True
        elif arg == "--random":
            opts["random"] = True
        elif arg == "--depth":
            i += 1
            opts["depth"] = int(argv[i])
        else:
            print("看不懂的参数：%s" % arg)
            print(__doc__)
            raise SystemExit(1)
        i += 1
    return opts


def show(board):
    print()
    print(board)
    print()


def main():
    opts = parse_args(sys.argv[1:])

    if opts["random"]:
        from engine import RandomAgent
        agent = RandomAgent()
        label = "随机对手"
    else:
        from engine import AlphaBetaAgent
        agent = AlphaBetaAgent(max_depth=opts["depth"])
        label = ("限深 %d 层 + 手工评估" % opts["depth"]) if opts["depth"] else "完美 AI（搜到终局）"

    human = 1 if opts["first"] else 2          # 1 = X 先手，2 = O 后手
    board = Board()

    print("=" * 52)
    print("井字棋 · 人机对战")
    print("对手：%s" % label)
    print("你执：%s" % ("X（先手）" if human == 1 else "O（后手）"))
    print("=" * 52)
    print("输入 0-8 落子（编号见棋盘下方），q 退出")

    while True:
        status, _ = game_status(board)
        if status != "进行中":
            show(board)
            print("对局结束：%s" % status)
            if status == "平局":
                print("（完美 AI 的对局通常以平局收场 —— 井字棋在双方最优下就是平局）")
            break

        show(board)

        if board.current_player == human:
            raw = input("轮到你，输入格子编号（0-8）：").strip()
            if raw in ("q", "quit", "exit"):
                print("退出。")
                return
            try:
                index = int(raw)
            except ValueError:
                print("『%s』不是数字。" % raw)
                continue
            if not board.is_legal(index):
                print("格子 %d 不能下。" % index)
                continue
            board.push(index)
        else:
            print("AI 思考中……")
            move, value = agent.choose(board)
            if move is None:
                print("AI 没有走法了。")
                break
            board.push(move)
            if hasattr(agent, "stats"):
                print("AI 走 %d（它给这个局面的分数：%s；%s）"
                      % (move, value, agent.stats))


if __name__ == "__main__":
    main()
