# -*- coding: utf-8 -*-
"""L02 数据测量：为备课拿到准确的数字（教师用，不属于课程）

跑法：
    cd src/part2_search
    python measure.py
"""

import sys
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PART1 = os.path.join(os.path.dirname(HERE), "part1_tictactoe")
sys.path.insert(0, PART1)

sys.stdout.reconfigure(encoding="utf-8")

from board import Board                      # noqa: E402
from rules import winner, is_full, game_status, X_WINS, O_WINS, DRAW  # noqa: E402
from constants import X, O, EMPTY, N_CELLS   # noqa: E402


# ======================================================================
# 1. 局面总数 / 对局总数 / 终局分布（穷举）
# ======================================================================
def enumerate_game_tree():
    """返回 (局面总数, 终局分布, 对局总数)"""
    seen_positions = set()
    endings = {X_WINS: 0, O_WINS: 0, DRAW: 0}
    total_games = 0

    def walk(cells, depth):
        nonlocal total_games
        seen_positions.add(tuple(cells))
        w = winner(cells)
        if w is not None:
            endings[X_WINS if w == X else O_WINS] += 1
            total_games += 1
            return
        if is_full(cells):
            endings[DRAW] += 1
            total_games += 1
            return
        player = X if depth % 2 == 0 else O
        for i in range(N_CELLS):
            if cells[i] == EMPTY:
                cells[i] = player
                walk(cells, depth + 1)
                cells[i] = EMPTY

    walk([EMPTY] * N_CELLS, 0)
    return len(seen_positions), endings, total_games


# ======================================================================
# 2. 节点计数版 minimax / alpha-beta
# ======================================================================
class Counter:
    def __init__(self):
        self.nodes = 0
        self.leaves = 0
        self.cutoffs = 0


def value_of(cells):
    """带值的终局判定：X 赢 +1，O 赢 -1，平局 0，未结束 None"""
    w = winner(cells)
    if w == X:
        return 1
    if w == O:
        return -1
    if is_full(cells):
        return 0
    return None


def minimax_count(cells, depth, cnt):
    """经典 minimax：X 取 max，O 取 min。返回局面价值。"""
    cnt.nodes += 1
    v = value_of(cells)
    if v is not None:
        cnt.leaves += 1
        return v
    if depth % 2 == 0:            # X 走，取最大
        best = -2
        for i in range(N_CELLS):
            if cells[i] == EMPTY:
                cells[i] = X
                best = max(best, minimax_count(cells, depth + 1, cnt))
                cells[i] = EMPTY
        return best
    else:                         # O 走，取最小
        best = 2
        for i in range(N_CELLS):
            if cells[i] == EMPTY:
                cells[i] = O
                best = min(best, minimax_count(cells, depth + 1, cnt))
                cells[i] = EMPTY
        return best


def alphabeta_count(cells, depth, alpha, beta, cnt):
    """alpha-beta：X 取 max，O 取 min。"""
    cnt.nodes += 1
    v = value_of(cells)
    if v is not None:
        cnt.leaves += 1
        return v
    if depth % 2 == 0:
        best = -2
        for i in range(N_CELLS):
            if cells[i] == EMPTY:
                cells[i] = X
                best = max(best, alphabeta_count(cells, depth + 1, alpha, beta, cnt))
                cells[i] = EMPTY
                alpha = max(alpha, best)
                if alpha >= beta:
                    cnt.cutoffs += 1
                    break
        return best
    else:
        best = 2
        for i in range(N_CELLS):
            if cells[i] == EMPTY:
                cells[i] = O
                best = min(best, alphabeta_count(cells, depth + 1, alpha, beta, cnt))
                cells[i] = EMPTY
                beta = min(beta, best)
                if alpha >= beta:
                    cnt.cutoffs += 1
                    break
        return best


def negamax_count(cells, depth, player, alpha, beta, cnt):
    """negamax + alpha-beta：站在 player 的立场，永远取最大。"""
    cnt.nodes += 1
    w = winner(cells)
    if w is not None:
        cnt.leaves += 1
        return 1 if w == player else -1
    if is_full(cells):
        cnt.leaves += 1
        return 0
    best = -2
    for i in range(N_CELLS):
        if cells[i] == EMPTY:
            cells[i] = player
            v = -negamax_count(cells, depth + 1, 3 - player, -beta, -alpha, cnt)
            cells[i] = EMPTY
            if v > best:
                best = v
            if best > alpha:
                alpha = best
            if alpha >= beta:
                cnt.cutoffs += 1
                break
    return best


# ======================================================================
# 3. 走法排序（对 alpha-beta 的影响）
# ======================================================================
def order_center_first(moves):
    """中心 -> 角 -> 边"""
    priority = {4: 0, 0: 1, 2: 1, 6: 1, 8: 1, 1: 2, 3: 2, 5: 2, 7: 2}
    return sorted(moves, key=lambda m: priority[m])


def order_edge_first(moves):
    """故意反过来：边 -> 角 -> 中心"""
    priority = {4: 2, 0: 1, 2: 1, 6: 1, 8: 1, 1: 0, 3: 0, 5: 0, 7: 0}
    return sorted(moves, key=lambda m: priority[m])


def alphabeta_ordered(cells, depth, player, alpha, beta, cnt, order):
    cnt.nodes += 1
    w = winner(cells)
    if w is not None:
        cnt.leaves += 1
        return 1 if w == player else -1
    if is_full(cells):
        cnt.leaves += 1
        return 0
    best = -2
    for i in order([j for j in range(N_CELLS) if cells[j] == EMPTY]):
        cells[i] = player
        v = -alphabeta_ordered(cells, depth + 1, 3 - player, -beta, -alpha, cnt, order)
        cells[i] = EMPTY
        if v > best:
            best = v
        if best > alpha:
            alpha = best
        if alpha >= beta:
            cnt.cutoffs += 1
            break
    return best


# ======================================================================
# 跑
# ======================================================================
if __name__ == "__main__":
    print("=" * 62)
    print("【1】井字棋有多大（穷举）")
    print("=" * 62)
    t0 = time.time()
    n_pos, endings, n_games = enumerate_game_tree()
    print("合法局面总数（含空盘）:", n_pos)
    print("可能的对局总数        :", n_games)
    print("终局分布              : X 赢 %d, O 赢 %d, 平局 %d"
          % (endings[X_WINS], endings[O_WINS], endings[DRAW]))
    print("穷举耗时              : %.2f 秒" % (time.time() - t0))
    print("注：如果双方都走最好，结果是 %s"
          % ("平局" if True else ""))

    print()
    print("=" * 62)
    print("【2】空盘上，三种算法的节点数对比")
    print("=" * 62)

    cnt = Counter()
    t0 = time.time()
    v = minimax_count([EMPTY] * N_CELLS, 0, cnt)
    t_minimax = time.time() - t0
    print("minimax（X 视角）      : 价值 %+d | 节点 %d | 叶 %d | 用时 %.3fs"
          % (v, cnt.nodes, cnt.leaves, t_minimax))

    cnt2 = Counter()
    t0 = time.time()
    v2 = alphabeta_count([EMPTY] * N_CELLS, 0, -2, 2, cnt2)
    t_ab = time.time() - t0
    print("alpha-beta（X 视角）   : 价值 %+d | 节点 %d | 叶 %d | 剪枝 %d | 用时 %.3fs"
          % (v2, cnt2.nodes, cnt2.leaves, cnt2.cutoffs, t_ab))

    cnt3 = Counter()
    t0 = time.time()
    v3 = negamax_count([EMPTY] * N_CELLS, 0, X, -2, 2, cnt3)
    t_ng = time.time() - t0
    print("negamax+ab（X 视角）   : 价值 %+d | 节点 %d | 叶 %d | 剪枝 %d | 用时 %.3fs"
          % (v3, cnt3.nodes, cnt3.leaves, cnt3.cutoffs, t_ng))

    print()
    print("数值一样吗：minimax=%+d  alpha-beta=%+d  negamax=%+d" % (v, v2, v3))
    print("节点数下降倍数：minimax / alpha-beta = %.1f 倍" % (cnt.nodes / cnt2.nodes))
    print("理论最优（完美排序，b^(d/2) 量级）: 井字棋 d=9, b≈5 -> 5^4.5 ≈ %.0f"
          % (5 ** 4.5))

    print()
    print("=" * 62)
    print("【3】走法排序对 alpha-beta 的影响（同一局面、同一算法）")
    print("=" * 62)
    for name, order in [("中心优先（好排序）", order_center_first),
                        ("边优先（坏排序）", order_edge_first)]:
        c = Counter()
        v = alphabeta_ordered([EMPTY] * N_CELLS, 0, X, -2, 2, c, order)
        print("  %s : 价值 %+d | 节点 %d | 剪枝 %d" % (name, v, c.nodes, c.cutoffs))

    c = Counter()
    v = alphabeta_count([EMPTY] * N_CELLS, 0, -2, 2, c)     # 按格子编号顺序 = 3,4,5,6,7,8
    print("  %s : 价值 %+d | 节点 %d | 剪枝 %d" % ("格子编号顺序", v, c.nodes, c.cutoffs))

    print()
    print("=" * 62)
    print("【4】五子棋为什么不行（深度爆炸的量级）")
    print("=" * 62)
    for b in (30, 60):
        for d in (4, 6, 8, 10):
            print("  分支因子 %2d，深度 %2d 层 -> %s 个局面"
                  % (b, d, "{:,}".format(b ** d)))
    print("  对照：银河系恒星数量约 10^11（1000 亿）")
    print("  对照：可观测宇宙原子数约 10^80")
