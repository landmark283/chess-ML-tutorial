# -*- coding: utf-8 -*-
"""arena.py —— 让两个智能体对战若干局，统计胜负

棋类 AI 的"分数"只有一种是有意义的：**胜率**。
不是 loss，不是准确率，是对战胜率。

这一课你会用它来：
    · 证明永远搜到终局的 AI，对战随机对手 1000 局零败
    · 看到"限深 + 手工评估"的 AI 会输棋 —— 从而理解 L03 为什么存在
"""

import random

from _paths import PART1  # noqa: F401
from board import Board
from rules import winner, is_full, X_WINS, O_WINS, DRAW
from constants import X, O


def play_one(agent_x, agent_o, opening=None):
    """让两个智能体下一局。agent_x 执 X 先手，agent_o 执 O。

    opening: 可选的固定开局（走法列表），用来做"同一局面、换算法"的对照实验。
    返回 'X' / 'O' / 'draw'
    """
    board = Board()
    if opening:
        for move in opening:
            board.push(move)

    while True:
        w = winner(board.cells)
        if w == X:
            return "X"
        if w == O:
            return "O"
        if is_full(board.cells):
            return "draw"

        agent = agent_x if board.current_player == X else agent_o
        move, _ = agent.choose(board)
        if move is None:
            return "draw"
        board.push(move)


def match(agent_a, agent_b, n_games=200, both_sides=True, seed=None):
    """让 A 和 B 对战 n_games 局。

    both_sides=True 时，**每个开局都换边再下一局**（A 先手一半、后手一半）。
    这很重要：棋类里先手优势巨大，不换边的话胜率根本没意义。

    返回一个统计字典。
    """
    if seed is not None:
        random.seed(seed)

    a_wins = b_wins = draws = 0
    for game in range(n_games):
        # 前半段 A 执 X，后半段 A 执 O
        a_is_x = (game % 2 == 0) if both_sides else True
        if a_is_x:
            result = play_one(agent_a, agent_b)
            if result == "X":
                a_wins += 1
            elif result == "O":
                b_wins += 1
            else:
                draws += 1
        else:
            result = play_one(agent_b, agent_a)
            if result == "X":
                b_wins += 1
            elif result == "O":
                a_wins += 1
            else:
                draws += 1

    total = a_wins + b_wins + draws
    return {
        "games": total,
        "a_wins": a_wins,
        "b_wins": b_wins,
        "draws": draws,
        "a_win_rate": a_wins / total,
        "b_win_rate": b_wins / total,
        "draw_rate": draws / total,
        # 棋类里常用的"得分率"：赢 1 分、平 0.5 分（和 Elo 计算一致）
        "a_score": (a_wins + 0.5 * draws) / total,
    }


def format_result(name_a, name_b, stats):
    return ("%s vs %s：%d 局 -> 胜 %d / 负 %d / 平 %d   "
            "（%s 得分率 %.1f%%）"
            % (name_a, name_b, stats["games"],
               stats["a_wins"], stats["b_wins"], stats["draws"],
               name_a, stats["a_score"] * 100))


def perfect_play_possible(agent):
    """检查这个智能体在空盘上的价值：0 = 完美（平局），+1 = 必胜，-1 = 必败。"""
    return agent.value(Board())
