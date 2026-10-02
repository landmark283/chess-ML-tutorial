# -*- coding: utf-8 -*-
"""tests/test_rules.py —— 规则引擎的测试

文件名叫 test_rules.py，但里面也测了 winner() 的 8 条线。
**规则代码是全项目最不能出错的地方**：它错了，L02 的搜索会一本正经地
搜出一个错误的"必胜"，而你会去怀疑搜索算法，白折腾一整天。
"""

from board import Board
from rules import (
    winner, is_full, game_status, is_over, has_winner,
    parse, board_from_text,
    X_WINS, O_WINS, DRAW, ONGOING,
)
from constants import EMPTY, X, O


def test_parse_ignores_separators():
    assert parse("X.O/.X./..O") == parse("X . O / . X . / . . O")
    assert len(parse(".../.../...")) == 9
    assert parse(".../.../...") == [EMPTY] * 9


def test_parse_rejects_bad_input():
    try:
        parse("X.O/.X./..")          # 只有 8 个格子
    except ValueError:
        pass
    else:
        raise AssertionError("格子数不足时应该报 ValueError")

    try:
        parse("X.O/.X./..Z")         # 不认识的字符
    except ValueError:
        pass
    else:
        raise AssertionError("出现看不懂的字符时应该报 ValueError")


def test_winner_detects_all_three_rows():
    assert winner(parse("XXX/.../...")) == X
    assert winner(parse(".../OOO/...")) == O
    assert winner(parse(".../.../XXX")) == X


def test_winner_detects_all_three_columns():
    assert winner(parse("X../X../X..")) == X
    assert winner(parse(".O./.O./.O.")) == O
    assert winner(parse("..X/..X/..X")) == X


def test_winner_detects_both_diagonals():
    """最容易漏的两条线。L01 的知识点测验会让你亲手补全它们。"""
    assert winner(parse("X../.X./..X")) == X      # 主对角线 ↘
    assert winner(parse("..O/.O./O..")) == O      # 副对角线 ↙


def test_winner_returns_none_on_ongoing_board():
    assert winner(parse("X.O/.X./..O")) is None
    assert winner(parse(".../.../...")) is None


def test_winner_needs_three_not_two():
    assert winner(parse("XX./.../...")) is None
    assert winner(parse("XO./OX./...")) is None


def test_is_full():
    assert is_full(parse("XOX/OXO/XOX"))
    assert not is_full(parse("XXO/OXO/XO."))     # 还剩一格


def test_game_status_ongoing():
    board = board_from_text("X../.O./...")
    assert game_status(board) == (ONGOING, None)
    assert not is_over(board)


def test_game_status_x_wins():
    board = board_from_text("XXX/OO./...")
    assert game_status(board) == (X_WINS, X)
    assert is_over(board)


def test_game_status_o_wins():
    board = board_from_text("XX./OOO/X..")     # 中间一行被 O 占满
    assert game_status(board) == (O_WINS, O)
    assert is_over(board)


def test_game_status_draw():
    # 5 个 X、4 个 O，满盘但没有任何一条线被占满 —— 这是真平局
    board = board_from_text("XOX/OXX/OXO")
    assert is_full(board.cells)
    assert winner(board.cells) is None
    assert game_status(board) == (DRAW, None)
    assert is_over(board)


def test_finished_game_is_detected_after_the_winning_move():
    """走完最后一手之后，状态必须立刻变成"结束"。"""
    b = Board()
    for move in [0, 3, 1, 4, 2]:      # X: 0,1,2 占满第一行
        b.push(move)
    assert game_status(b) == (X_WINS, X)


def test_board_from_text_restores_current_player():
    # 空格为 0 手 -> 轮到 X；一个 X -> 轮到 O；X 和 O 各一个 -> 又轮到 X
    assert board_from_text(".../.../...").current_player == X
    assert board_from_text("X../.../...").current_player == O
    assert board_from_text("XO./.../...").current_player == X
    assert len(board_from_text("XOX/OX./...")) == 5


def test_has_winner_matches_winner():
    assert has_winner(parse("XXX/.../...")) is True
    assert has_winner(parse(".../.../...")) is False


def test_who_moves_first_decides_who_can_win():
    """一个容易被忽略的事实：X 先下，所以终局时 X 一定比 O 多一个子。

    推论：任何"O 的子和 X 一样多、却是 O 赢"的局面都是不可能出现的。
    `board_from_text` 会拒绝这种局面 —— 这是它在帮我们挡错。
    """
    assert parse("XXX/.../...").count(X) == 3    # X 三连获胜时用掉 3 子
    assert parse("XX./OOO/X..").count(X) == 3    # O 三连获胜时，X 下了 3 手
    assert parse("XOX/OXX/OXO").count(X) == 5    # 平局：9 格全满，X 5 子 O 4 子

    try:
        board_from_text("OOO/X../...")     # O 3 子、X 只有 1 子，绝无可能
    except ValueError:
        pass
    else:
        raise AssertionError("O 多于 X 的局面应该被拒绝")


def test_board_from_text_rejects_impossible_position():
    # O 比 X 还多一个 -> 不可能出现（X 先下）
    try:
        board_from_text("OOO/.../...")
    except ValueError:
        pass
    else:
        raise AssertionError("O 多于 X 的局面应该被拒绝")


def test_board_from_text_board_is_playable():
    b = board_from_text("X../.../...")
    assert not b.is_legal(0)
    b.push(4)
    assert b.cells[4] == O
    assert b.current_player == X
