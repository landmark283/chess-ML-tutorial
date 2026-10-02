# -*- coding: utf-8 -*-
"""tests/test_board.py —— 棋盘数据结构的测试

怎么读这些测试：每个 test_xxx 函数 = 一条"我对代码的断言"。
测试通过 = 断言成立；断言失败 = 我写的代码没做到我说的事。

注意这些是**最朴素的测试**：只用 assert，没有装任何测试框架。
它同时能被 `run_tests.py`（本课自带）和 `pytest`（你以后可以装）执行。
"""

import copy

from board import Board, to_index, to_coord, as_2d, from_2d
from constants import EMPTY, X, O, N_CELLS


def test_new_board_is_all_empty():
    b = Board()
    assert b.cells == [EMPTY] * N_CELLS
    assert len(b.cells) == 9
    assert len(b.history) == 0
    assert len(b) == 0


def test_display_shows_nine_empty_cells():
    b = Board()
    text = str(b)
    assert text.count("·") == 9
    assert "X" not in text and "O" not in text


def test_coordinate_round_trip():
    # 9 个格子，转过去再转回来，必须一模一样
    for index in range(N_CELLS):
        row, col = to_coord(index)
        assert to_index(row, col) == index
    assert to_coord(0) == (0, 0)   # 左上
    assert to_coord(4) == (1, 1)   # 正中
    assert to_coord(8) == (2, 2)   # 右下
    assert to_coord(5) == (1, 2)   # 中排最右


def test_2d_and_1d_are_the_same_board():
    b = Board()
    b.push(0)
    b.push(4)
    rows = as_2d(b.cells)
    assert rows[0][0] == X
    assert rows[1][1] == O
    assert from_2d(rows) == b.cells


def test_rows_are_independent_not_aliases():
    """K1.3 的病灶：`[[0]*3]*3` 造出来的三行是同一行。

    这个测试不是在测我的代码，是在**演示那个 bug**：
    buggy 是错的，good 是对的，两者只差一个写法。
    """
    buggy = [[EMPTY] * 3] * 3      # ❌ 三个引用指向同一个列表
    good = [[EMPTY] * 3 for _ in range(3)]   # ✅ 三个独立的列表

    buggy[0][0] = X
    good[0][0] = X

    assert buggy[1][0] == X     # 第 1 行跟着变了 —— 这就是 bug
    assert buggy[2][0] == X     # 第 2 行也变了
    assert good[1][0] == EMPTY  # 正常实现：只有第 0 行变
    assert good[2][0] == EMPTY
    assert buggy[0] is buggy[1]     # 它们根本是同一个对象
    assert good[0] is not good[1]   # 这才叫"三行"


def test_current_player_alternates():
    b = Board()
    assert b.current_player == X
    b.push(0)
    assert b.current_player == O
    b.push(1)
    assert b.current_player == X
    b.pop()
    assert b.current_player == O
    b.pop()
    assert b.current_player == X


def test_legal_moves_shrink_as_board_fills():
    b = Board()
    assert b.legal_moves() == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    b.push(4)
    assert b.legal_moves() == [0, 1, 2, 3, 5, 6, 7, 8]
    assert not b.is_legal(4)


def test_push_then_pop_restores_everything():
    b = Board()
    before = list(b.cells)
    b.push(7)
    assert b.cells[7] == X
    b.pop()
    assert b.cells == before
    assert b.history == []


def test_many_pushes_and_pops_come_back_to_start():
    b = Board()
    moves = [4, 0, 8, 2, 6, 1, 3, 5]
    for m in moves:
        b.push(m)
    for _ in moves:
        b.pop()
    assert b.cells == [EMPTY] * N_CELLS
    assert len(b.history) == 0
    assert b.current_player == X


def test_push_on_occupied_cell_raises():
    b = Board()
    b.push(4)
    try:
        b.push(4)
    except ValueError:
        pass
    else:
        raise AssertionError("在已占据的格子上落子，应该报 ValueError")


def test_push_out_of_range_raises():
    b = Board()
    for bad in (-1, 9, 100):
        try:
            b.push(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("落子 %r 越界，应该报 ValueError" % (bad,))


def test_pop_on_empty_board_raises():
    b = Board()
    try:
        b.pop()
    except ValueError:
        pass
    else:
        raise AssertionError("空棋盘悔棋，应该报 ValueError")


def test_copy_is_independent():
    """给 L02 的搜索埋的伏笔：搜索要试很多种走法，靠的就是"拷贝一份接着试"。

    这里同时对比浅拷贝和深拷贝 —— 它就是 K1.3 那个陷阱的另一副面孔：
    浅拷贝只复制最外面那层容器，里面装的东西还是同一批。
    """
    b = Board()
    b.push(4)                   # 第 1 手：X 占中心
    b.push(0)                   # 第 2 手：O 占左上

    assert b.cells[0] == O      # 注意！第 2 手是 O，不是 X
    assert b.cells[4] == X

    shallow = copy.copy(b)      # 浅拷贝：cells 和 b.cells 是同一个列表对象
    deep = copy.deepcopy(b)     # 深拷贝：里里外外全是新的

    b.push(8)                   # 第 3 手：X 占右下
    assert b.cells[8] == X

    assert shallow.cells is b.cells     # 浅拷贝露馅了：它们共享同一个 cells
    assert shallow.cells[8] == X        # 所以原棋盘一动，浅拷贝也跟着变

    assert deep.cells is not b.cells    # 深拷贝是真正独立的
    assert deep.cells[8] == EMPTY
    assert len(deep.history) == 2
    assert len(b.history) == 3
