# -*- coding: utf-8 -*-
"""eval_functions.py —— 手工评估函数（K2.6 的主角）

在没有搜到终局的时候，搜索算法必须"停下来，猜一个分数"。
猜分数的那个函数就叫**评估函数**（evaluation function）。

本课先手写两个版本，用它们来感受"手工调权重"有多难受 ——
这正是 L03 要换成"从数据学出来"的原因。
"""

from _paths import PART1  # noqa: F401
from constants import EMPTY, X, O, LINES


def material_score(cells, player):
    """版本 1：只数子。

    `player` 是"从谁的立场看"。返回正数表示对 player 有利。

    井字棋里这个函数几乎没用 —— 因为双方子数最多差 1。
    写出来是为了让你看到"最简单的评估函数长什么样"。
    """
    mine = cells.count(player)
    theirs = cells.count(3 - player)
    return (mine - theirs) / 9.0


def evaluate(cells, player):
    """版本 2：数"每条线上的潜力"。

    对 8 条线各看一眼：
        · 这条线上有几个我的子、几个对手的子？
        · 如果只有我有子，这条线就是**我的潜在威胁**，分值 = 我这几个子的平方
        · 如果只有对手有子，就是**对手的威胁**，分值取负
        · 双方都有子 -> 这条线废了，0 分

    为什么要平方？因为"2 个子在一条线上"比"1 个子"危险得多（差一步就赢）。
    平方让 2 -> 4，差距被拉开。

    返回一个大致落在 [-1, 1] 的实数。
    """
    score = 0.0
    for a, b, c in LINES:
        mine = 0
        theirs = 0
        for idx in (a, b, c):
            v = cells[idx]
            if v == player:
                mine += 1
            elif v != EMPTY:
                theirs += 1
        if mine and theirs:
            continue                       # 这条线废了
        if mine:
            score += mine * mine
        elif theirs:
            score -= theirs * theirs
    return score / 20.0                     # 缩放到 1 附近


def evaluate_centered(cells, player):
    """版本 3：在版本 2 的基础上，额外奖励"占中心 / 占角"。

    这是"手工特征工程"的味道：我凭直觉加一项，再凭感觉调权重。

    ⚠️ **这里藏着一个真实的坑，我故意留着它给你看。**

    第一版我写的是"占中心就 +0.05"。跑测试的时候发现：加了这一项之后，
    `evaluate_centered(占中心的局面) < evaluate(占中心的局面)` —— **分数反而降了**！

    为什么？因为**中心同时被算了两次**：
        ① "线上的潜力"那一项里，中心已经在 4 条线上贡献了分数
        ② 现在又额外加一遍
    重复计算让权重的相对大小完全乱掉。

    这不是我编的例子 —— 这是**手工设计评估函数时最常见的一类 bug**，
    而且它不会报错，只会让 AI 变弱。修好的做法是：**让附加项只做"线上潜力看不出的事"**，
    也就是"同样条数下，谁占着更关键的位置"这个**平局决胜**因素。

    （L07 会正式讲"特征之间的重复计算"，以及怎么用消融实验发现它。）
    """
    base = evaluate(cells, player)

    # 只看"位置本身"，不看线 —— 这才是和上面不重叠的信息
    positional = 0.0
    if cells[4] == player:
        positional += 1.0
    elif cells[4] != EMPTY:
        positional -= 1.0
    for corner in (0, 2, 6, 8):
        if cells[corner] == player:
            positional += 0.5
        elif cells[corner] != EMPTY:
            positional -= 0.5

    return base + 0.01 * positional        # 权重很小：只用来打破平局
