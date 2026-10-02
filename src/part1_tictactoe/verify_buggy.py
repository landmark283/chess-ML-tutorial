# -*- coding: utf-8 -*-
"""verify_buggy.py —— 确认 buggy.py 里确实只有那 3 个 bug（教师用）

它把 buggy.py 的行为摆出来，让"预期 / 实际"的差异一目了然。
学生不需要读这个文件 —— 但如果你想，它其实是一份"怎么写对照测试"的示范：
    正确版本的行为  ==  我写的 assert
"""

import sys
import os
import importlib.util

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


buggy = load("buggy", os.path.join(HERE, "buggy.py"))

print("=== bug ①  new_game() 的三行是不是同一个对象 ===")
game = buggy.new_game()
ids = [id(row) for row in game["board"]]
print("  三行的 id ：", ids)
print("  实际      ：共用同一个列表 =", len(set(ids)) == 1)
print("  应该是    ：三行互相独立（三个不同的 id）")
print("  后果      ：一格被改，九格全乱")

print("\n=== bug ②  is_legal() 对已占据格子的回答 ===")
g = buggy.new_game()
buggy.push(g, 0, 0)          # X 占左上
print("  (0,0) 已经下了 X，再问它能不能下：")
print("  实际      ：", buggy.is_legal(g, 0, 0), "（True 是错的）")
print("  应该是    ：False")
print("  后果      ：同一格被反复覆盖，历史里的手数和棋盘对不上")

print("\n=== bug ③  winner() 对空盘的回答 ===")
empty = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
print("  winner(空盘) 实际：", buggy.winner(empty), "（0 是错的，空 != 有人赢）")
print("  winner(空盘) 应为： None")
print("  原因      ：EMPTY == EMPTY 也是 True，所以‘三格相同’必须先排除空格")
print("  后果      ：一开局 AI 就以为已经有人赢了")

print("\n=== 其他行为应该是对的（用不共享行的正确棋盘来验） ===")
good = [[1, 2, 1], [2, 1, 1], [2, 1, 2]]     # 满盘平局
print("  平局盘 winner   ：", buggy.winner(good), "（应为 None）")
good2 = [[1, 1, 1], [2, 2, 0], [0, 0, 0]]    # X 占满第一行
print("  X 三连盘 winner ：", buggy.winner(good2), "（应为 1 = X）")
g = buggy.new_game()
for r, c in [(1, 1), (0, 0), (1, 0)]:
    buggy.push(g, r, c)
print("  悔棋前 history  ：", g["history"])
buggy.pop(g)
print("  悔棋后 history  ：", g["history"], "（应为 2 手）")
print("  悔棋后该谁下     ：", buggy.turn(g), "（应为 X）")

