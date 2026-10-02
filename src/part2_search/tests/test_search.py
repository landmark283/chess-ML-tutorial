# -*- coding: utf-8 -*-
"""tests/test_search.py —— L02 的测试

测试的重点和 L01 完全不同。L01 测的是"数据结构和规则对不对"，
这里测的是**算法的正确性**，而搜索算法的正确性有一条金标准：

    ❗ 剪枝/优化/重写以后，答案必须一模一样。

所以你会看到不少"两个实现必须给出同一个值"的测试。
这不是形式主义 —— 这是唯一能证明剪枝没写错的办法。
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for path in (ROOT, os.path.join(os.path.dirname(ROOT), "part1_tictactoe")):
    if path not in sys.path:
        sys.path.insert(0, path)

import _paths  # noqa: F401,E402  （把 part1 加进模块搜索路径）

from board import Board                                     # noqa: E402
from constants import EMPTY, X, O, LINES, N_CELLS           # noqa: E402
from rules import winner, is_full, parse                    # noqa: E402
from eval_functions import evaluate, evaluate_centered, material_score  # noqa: E402
from engine import (MinimaxAgent, NegamaxAgent, AlphaBetaAgent,        # noqa: E402
                    RandomAgent, no_ordering)
from arena import match, play_one                            # noqa: E402


# ----------------------------------------------------------------------
# 工具
# ----------------------------------------------------------------------
def board_with(cells):
    """从一个 9 格的列表造一个可继续下的 Board（history 靠填空格数补上）"""
    b = Board()
    b.cells = list(cells)
    n_moves = N_CELLS - b.cells.count(EMPTY)
    b.history = [0] * n_moves
    return b


def play_moves(moves, cells=None):
    """按顺序落子，造一个**合法**的局面。

    比 `board_with` 更可靠：`current_player` 是按真实手数推出来的，
    不会出现"棋盘上 O 有 3 个子，却轮到 X"这种自相矛盾的局面。
    """
    b = Board()
    if cells is not None:
        b.cells = list(cells)
        b.history = [0] * (N_CELLS - b.cells.count(EMPTY))
    for m in moves:
        b.push(m)
    return b


def all_unfinished_boards(max_depth=6):
    """穷举所有"还没分出胜负"的局面，返回 [(cells 元组, 该谁走)]"""
    out = []

    def walk(cells, depth):
        if winner(cells) is not None or is_full(cells):
            return
        out.append((tuple(cells), X if depth % 2 == 0 else O))
        if depth >= max_depth:
            return
        player = X if depth % 2 == 0 else O
        for i in range(N_CELLS):
            if cells[i] == EMPTY:
                cells[i] = player
                walk(cells, depth + 1)
                cells[i] = EMPTY

    walk([EMPTY] * N_CELLS, 0)
    return out


# ----------------------------------------------------------------------
# 评估函数
# ----------------------------------------------------------------------
def test_material_score_counts_pieces():
    empty = [EMPTY] * N_CELLS
    assert material_score(empty, X) == 0
    one_x = [X] + [EMPTY] * 8
    assert material_score(one_x, X) > 0
    assert material_score(one_x, O) < 0
    # 对称：从 X 看和从 O 看，符号相反、大小相同
    two = [X, O] + [EMPTY] * 7
    assert material_score(two, X) == -material_score(two, O)


def test_evaluate_scores_threats():
    """我的 2 连要比我的 1 连分高；而且**平方**拉开差距（2 连 > 1 连的 2 倍）"""
    one = parse("X../.../...")
    two = parse("XX./.../...")
    assert evaluate(two, X) > evaluate(one, X)
    assert evaluate(two, X) > 2 * evaluate(one, X)      # 平方效应


def test_evaluate_is_antisymmetric():
    """零和：从我方看的分 = 从对方看的分的相反数"""
    for text in ["X.O/.X./..O", "XX./.O./...", ".../.../...", "XO./OX./..."]:
        cells = parse(text)
        assert abs(evaluate(cells, X) + evaluate(cells, O)) < 1e-9


def test_evaluate_centered_rewards_center():
    """占中心应该加分 —— 这是 evaluate_centered 存在的理由。

    ⚠️ 这个测试还记录了一个真实踩过的坑：
    第一版 evaluate_centered 写的是"占中心 +0.05"，结果**分数反而降了** ——
    因为中心已经在"线上的潜力"里算过一遍，加的那一项是**重复计算**。
    测试当场就把它抓出来了（`assert 加 >= 不加` 挂了）。
    """
    empty = [EMPTY] * N_CELLS
    assert evaluate_centered(empty, X) == evaluate(empty, X)   # 没有子时不该有差别

    center_mine = parse(".../.X./...")
    assert evaluate_centered(center_mine, X) > evaluate(center_mine, X)
    assert evaluate_centered(center_mine, X) > evaluate_centered(empty, X)

    corner_mine = parse("X../.../...")
    assert evaluate_centered(corner_mine, X) > evaluate(corner_mine, X)

    # 还是零和的
    for cells in (center_mine, corner_mine, empty):
        assert abs(evaluate_centered(cells, X) + evaluate_centered(cells, O)) < 1e-9


# ----------------------------------------------------------------------
# 最小最大 / 负最大：等价性
# ----------------------------------------------------------------------
def test_minimax_value_on_empty_board_is_draw():
    """井字棋的标准答案：双方最优 -> 平局 -> 0"""
    assert MinimaxAgent().value(Board()) == 0


def test_negamax_value_on_empty_board_is_draw():
    assert NegamaxAgent().value(Board()) == 0


def test_minimax_and_negamax_agree_on_every_position():
    """minimax 永远以 X 的立场（+1 = X 赢）；negamax 以"该走的人"的立场。

    两者的换算关系：**minimax 的值 = negamax 的值 × (该走的人是 X ? +1 : −1)**

    这一类"两套实现必须能对上"的测试，是发现**视角/符号错误**的唯一有效手段。
    minimax 的符号搞反了程序照样跑 —— 只有这种对照能把它钉死。
    """
    minimax = MinimaxAgent()
    negamax = NegamaxAgent()
    checked = 0
    for cells, player in all_unfinished_boards():
        b = board_with(cells)
        assert b.current_player == player, "测试自己构造错了：%r" % (cells,)
        m = minimax.value(b)
        n = negamax.value(b)
        expected = n if player == X else -n
        assert m == expected, "局面 %r 该 %s 走：minimax=%d negamax=%d" % (cells, player, m, n)
        checked += 1
    assert checked > 500, "检查的局面太少了（只有 %d 个），穷举是不是没跑对？" % checked


# ----------------------------------------------------------------------
# 剪枝：不改变答案（本课最重要的测试）
# ----------------------------------------------------------------------
def test_alphabeta_agrees_with_unpruned_negamax():
    """剪枝版和完全不剪枝版，在同一批局面上必须给出**逐位相同**的值。"""
    pruned = AlphaBetaAgent()
    raw = AlphaBetaAgent(use_pruning=False, ordering=no_ordering)
    checked = 0
    for cells, player in all_unfinished_boards():
        b = board_with(cells)
        v1 = pruned.value(b)
        v2 = raw.value(b)
        assert v1 == v2, "剪枝出错！局面 %r：剪枝=%d 不剪枝=%d" % (cells, v1, v2)
        checked += 1
    assert checked > 500


def test_alphabeta_prunes_but_same_value_on_empty_board():
    pruned = AlphaBetaAgent()
    raw = AlphaBetaAgent(use_pruning=False, ordering=no_ordering)
    v1 = pruned.value(Board())
    n1 = pruned.stats.nodes
    v2 = raw.value(Board())
    n2 = raw.stats.nodes

    assert v1 == v2 == 0
    assert n1 < n2, "剪枝应该看得更少：%d vs %d" % (n1, n2)
    assert pruned.stats.cutoffs > 0
    assert raw.stats.cutoffs == 0


def test_move_ordering_reduces_nodes_without_changing_value():
    """走法排序也是"只改算了多少、不改算出什么" """
    ordered = AlphaBetaAgent()                                  # 中心优先
    unordered = AlphaBetaAgent(ordering=no_ordering)
    v1 = ordered.value(Board())
    n1 = ordered.stats.nodes
    v2 = unordered.value(Board())
    n2 = unordered.stats.nodes

    assert v1 == v2 == 0
    assert n1 < n2, "中心优先应该更省：%d vs %d" % (n1, n2)


# ----------------------------------------------------------------------
# 走法选择的正确性
# ----------------------------------------------------------------------
def test_perfect_agent_takes_immediate_win():
    """能一步赢就必须赢（这是最容易写错的地方之一）"""
    b = board_with(parse("XX./OO./..."))      # X 走 2 就赢
    move, value = AlphaBetaAgent().choose(b)
    assert move == 2
    assert value == 1


def test_perfect_agent_blocks_immediate_loss():
    """对手下一步就赢，必须挡住"""
    b = board_with(parse("OO./X../..."))      # O 有两个子在 0,1，X 必须堵 2
    move, value = AlphaBetaAgent().choose(b)
    assert move == 2, "该堵 2，它却走了 %r" % (move,)


def test_perfect_agent_values_a_won_position_correctly():
    """同一个棋盘，"该谁走"不同，价值就不同 —— 而且**符号会翻**。

    下面这些局面都用"按顺序落子"造出来（`play_moves`），
    所以"该谁走"是从规则推出来的，不是我硬凑的。
    """
    # ① X 中心 + O 角 -> 该 X 走。X 的正确下法是走另一个角，结果是平局
    b = play_moves([4, 0])
    assert b.current_player == X
    assert AlphaBetaAgent().value(b) == 0

    # ② X 中心 + O 角 + X 走边 -> 该 O 走。这个局面是**平局**，不是 O 胜！
    #    （O 唯一能守和的走法是 6。写成测试的时候我以为 O 赢了，
    #      是穷举 solver 纠正了我 —— 所以下面 ③ 那个才是真正的"必败局面"。）
    b = play_moves([4, 0, 2])
    assert b.current_player == O
    assert AlphaBetaAgent().value(b) == 0
    assert MinimaxAgent().value(b) == 0

    # ③ X 走 0、3（自己排一线），但 O 抢到 6、7 造出活二 -> 该 X 走，而 **X 已经输了**
    #    （这组走法是我用穷举 solver 搜出来的：4 手局面里 X 必败的那些之一。
    #      想自己找一个的话，可以写个穷举脚本打印所有"X 必败"的局面。）
    b = play_moves([0, 6, 3, 7])
    assert b.current_player == X
    assert AlphaBetaAgent().value(b) == -1, "这个局面 X 必败"
    assert NegamaxAgent().value(b) == -1
    assert MinimaxAgent().value(b) == -1, "minimax 以 X 为准，也是 -1"

    # ④ 同一个棋盘、硬说成"该 O 走" —— 符号立刻翻过来
    b = play_moves([0, 6, 3, 7])
    b.history = [0] * 5                      # 变成 5 手 -> 该 O 走
    assert AlphaBetaAgent().value(b) == 1

    # ⑤ 但注意：如果 X 第三手走了角（8），局面是平局
    b = play_moves([4, 0, 8])
    assert b.current_player == O
    assert AlphaBetaAgent().value(b) == 0


def test_value_of_already_finished_position():
    """给 value() 一个已经分出胜负的局面，它也得给对话（不能崩）

    注意 value() 的立场是"**该走的那个人**"：
        OOO/X../...  3 个 O + 1 个 X = 4 手 -> 该 X 走；O 已经赢了 -> 对 X 是 -1
    """
    assert AlphaBetaAgent().value(board_with(parse("OOO/X../..."))) == -1
    assert AlphaBetaAgent().value(board_with(parse("XOX/OXX/OXO"))) == 0   # 满盘平局

    # 顺便记住一个反直觉的事实：**同一个棋盘，"该谁走"不同，价值就不同。**
    #   X.X/.X./O..  3 个 X + 1 个 O = 4 手 -> 该 X 走，X 有双威胁 -> 必胜 (+1)
    #   X.X/.X./O..  如果硬说成"该 O 走"，那就是 -1（O 视角下必败）
    assert AlphaBetaAgent().value(board_with(parse("X.X/.X./O.."))) == 1
    b = board_with(parse("X.X/.X./O.."))
    b.history = [0] * 5                      # 硬凑成 5 手 -> 该 O 走
    assert AlphaBetaAgent().value(b) == -1


def test_agent_never_returns_illegal_move():
    perfect = AlphaBetaAgent()
    for cells, player in all_unfinished_boards(max_depth=4)[:200]:
        b = board_with(cells)
        move, _ = perfect.choose(b)
        assert move in b.legal_moves(), "局面 %r 给出了非法走法 %r" % (cells, move)


# ----------------------------------------------------------------------
# 限深搜索
# ----------------------------------------------------------------------
def test_depth_limited_agent_returns_legal_move():
    for depth in (1, 2, 3):
        agent = AlphaBetaAgent(max_depth=depth)
        b = Board()
        move, _ = agent.choose(b)
        assert move in b.legal_moves()


def test_depth_limited_agent_calls_evaluation():
    """限深之后一定会调用评估函数 —— 这正是"猜"的来源"""
    agent = AlphaBetaAgent(max_depth=2)
    agent.value(Board())
    assert agent.stats.evals > 0, "限深搜索居然没调用评估函数？"


def test_depth_limited_still_wins_in_one():
    """限深也不能看不见"下一步就赢" """
    for depth in (1, 2, 3):
        agent = AlphaBetaAgent(max_depth=depth)
        b = board_with(parse("XX./OO./..."))
        move, _ = agent.choose(b)
        assert move == 2, "限深 %d 层居然没看见必胜手，走了 %r" % (depth, move)


# ----------------------------------------------------------------------
# 对战平台
# ----------------------------------------------------------------------
def test_random_agent_plays_legal_moves():
    agent = RandomAgent()
    for _ in range(20):
        b = Board()
        move, _ = agent.choose(b)
        assert move in b.legal_moves()


def test_play_one_terminates_with_a_result():
    result = play_one(RandomAgent(), RandomAgent())
    assert result in ("X", "O", "draw")


def test_match_counts_add_up():
    stats = match(RandomAgent(), RandomAgent(), n_games=20, seed=1)
    assert stats["games"] == 20
    assert stats["a_wins"] + stats["b_wins"] + stats["draws"] == 20
    assert abs(stats["a_score"] - (stats["a_wins"] + 0.5 * stats["draws"]) / 20) < 1e-9


def test_match_is_deterministic_with_seed():
    s1 = match(RandomAgent(), RandomAgent(), n_games=30, seed=42)
    s2 = match(RandomAgent(), RandomAgent(), n_games=30, seed=42)
    assert s1 == s2, "同一个 seed 应该给出同一批对局"


def test_perfect_agent_beats_random_handily():
    stats = match(AlphaBetaAgent(), RandomAgent(), n_games=100, both_sides=False, seed=3)
    assert stats["b_wins"] == 0, "完美 AI 输给了随机对手 %d 局" % stats["b_wins"]
    assert stats["a_score"] > 0.9


def test_perfect_agent_never_loses_to_perfect_agent():
    stats = match(AlphaBetaAgent(), AlphaBetaAgent(), n_games=20, both_sides=True, seed=5)
    assert stats["a_wins"] == 0 and stats["b_wins"] == 0
    assert stats["draws"] == 20
