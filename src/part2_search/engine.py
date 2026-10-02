# -*- coding: utf-8 -*-
"""engine.py —— 搜索智能体（本课的主角）

三种算法在同一个文件里，方便你对照着读：

    MinimaxAgent      经典 minimax：X 取 max，O 取 min
    NegamaxAgent      negamax：永远取 max，靠符号翻转表达对手立场
    AlphaBetaAgent    negamax + alpha-beta 剪枝（本课最终用的那个）

三种都是"能搜多深就搜多深"；`max_depth` 用来限制深度（K2.6 会用到）。

三个通用能力，每个智能体都有：
    .choose(board)      返回这一步走哪（0..8 的编号）
    .value(board)       返回这个局面的分数（正 = 对我有利）
    .stats              搜索统计（看了多少个节点、剪掉多少次……）
"""

import random

from _paths import PART1  # noqa: F401  （导入即把 part1 加进模块搜索路径）
from constants import EMPTY, X, O, N_CELLS
from rules import winner, is_full
from eval_functions import evaluate, material_score


# ----------------------------------------------------------------------
# 走法排序
# ----------------------------------------------------------------------
def center_corner_edge(moves):
    """把走法按"中心 -> 角 -> 边"排好。

    这是本课能拿到的最简单也最有效的启发：
    井字棋里中心最强、角次之、边最弱，先搜强的，剪枝效率高得多。
    （K2.4 实测：空盘上节点数 18297 -> 7275）
    """
    priority = {4: 0, 0: 1, 2: 1, 6: 1, 8: 1, 1: 2, 3: 2, 5: 2, 7: 2}
    return sorted(moves, key=lambda m: priority[m])


def no_ordering(moves):
    """不排序，按格子编号来。"""
    return moves


# ----------------------------------------------------------------------
# 基类：公共部分
# ----------------------------------------------------------------------
class SearchStats:
    """搜索统计。没有它，你只能靠"感觉变快了"，而感觉不可信。"""

    def __init__(self):
        self.nodes = 0        # 访问过多少个局面
        self.leaves = 0       # 有多少个是终局（直接能判胜负）
        self.cutoffs = 0      # 发生了多少次剪枝
        self.evals = 0        # 调用了几次评估函数（限深搜索才用得上）

    def reset(self):
        self.__init__()

    def __str__(self):
        return ("节点 %d | 终局 %d | 剪枝 %d | 评估 %d"
                % (self.nodes, self.leaves, self.cutoffs, self.evals))


class BaseAgent:
    """三个智能体的公共外壳：处理"轮到谁"、终局判定、限深时的评估。

    子类只需要实现 `_search(cells, player, depth, alpha, beta)`。
    """

    name = "base"

    def __init__(self, max_depth=None, ordering=no_ordering):
        """
        max_depth : None = 一直搜到终局；数字 = 最多再往下搜这么多层
        ordering  : 走法排序函数
        """
        self.max_depth = max_depth
        self.ordering = ordering
        self.stats = SearchStats()

    # ---- 对外接口 ----
    def value(self, board):
        """评估当前局面对"该走的那一方"的价值（+1 必胜 / 0 平局 / -1 必败）。

        ⚠️ 头两行处理的是"这个局面本身已经结束了"的情况。
        搜索算法假设"轮到我了，我要选一步"，所以它们**不能**处理终局。
        但 `value()` 是给人调用的通用接口，可能被递进一个终局 —— 于是它必须先自己判一遍。

        这类"底层假设"没写清楚导致的崩溃，比算法写错更难找。
        所以每个对外函数都要问一句：**调用的人可能拿什么奇怪的输入来烦我？**
        """
        self.stats.reset()

        w = winner(board.cells)
        if w is not None:
            return 1 if w == board.current_player else -1
        if is_full(board.cells):
            return 0

        return self._search(board.cells, board.current_player,
                            depth=0, alpha=-2, beta=2)

    def choose(self, board):
        """选一步走。返回 (格子编号, 价值)；没有合法走法时返回 (None, None)。"""
        self.stats.reset()

        if winner(board.cells) is not None or is_full(board.cells):
            return None, None                  # 这局已经结束了，没得走

        me = board.current_player
        best_value = -2
        best_moves = []

        for move in self.ordering(board.legal_moves()):
            board.push(move)
            # 对手的立场看，价值要翻转
            value = -self._search(board.cells, board.current_player,
                                  depth=1, alpha=-2, beta=2)
            board.pop()

            if value > best_value:
                best_value = value
                best_moves = [move]
            elif value == best_value:
                best_moves.append(move)

        if not best_moves:
            return None, None
        # 同样好的走法里随机挑一个，免得每局都下成同一盘
        return random.choice(best_moves), best_value

    # ---- 子类实现 ----
    def _search(self, cells, player, depth, alpha, beta):
        raise NotImplementedError


# ----------------------------------------------------------------------
# 1. minimax（经典写法：max 和 min 各写一套）
# ----------------------------------------------------------------------
class MinimaxAgent(BaseAgent):
    """X 取最大、O 取最小。**它的价值永远以 X 的立场表达**。

    这是最贴近直觉的写法，也是代码最长的那种：
    递归里要判断"现在是谁走"，两套循环几乎一模一样，只是一个 max 一个 min。

    ⚠️ **注意 `value()` 里那个 `root_player` 的处理。**

    经典 minimax 的返回值是一律"以 X 为准"的（+1 = X 赢）。
    所以当一个**X 已经赢了的局面**递进来、而此刻轮到 O 走时，
    直接调 `_minimax` 会返回 +1 —— 可在 negamax 的语义里，
    这个局面是"该走的人（O）已经输了"，应该是 −1。

    这就是 minimax 那个"视角不统一"的毛病第一次咬人：
    **同一个局面，两种算法的返回值符号相反**，而你必须靠脑子记住这件事。
    K2.3 的 negamax 把这个约定彻底消掉了，代价只是每次多一个负号。
    """

    name = "minimax"

    def value(self, board):
        """返回"**这个局面本身**对 outcome 的判定"：X 赢 +1 / 平 0 / O 赢 −1；
        还没结束就用 minimax 算下去（同样以 X 为准）。

        ⚠️ **`depth` 的约定（踩过坑，写清楚在这里）**

        `_minimax(cells, depth)` 里的 `depth` 不是"我还想再搜几层"，
        而是"**这个局面总共走了多少手**"。因为"轮到谁"是靠 `depth % 2` 推的。

        所以调用时必须传**这个局面自己的手数**，而不能从 0 开始 ——
        否则一个"已经走了 3 手、轮到 O"的局面会被当成"轮到 X"来分析，
        算出来的值完全是错的（而且是**静默**错的：程序照跑，结果离谱）。

        这个 bug 就是测试抓出来的：`test_perfect_agent_values_a_won_position_correctly`
        报出"该 O 走的局面，value() 给了 +1"，而穷举的答案是 0。
        """
        self.stats.reset()

        w = winner(board.cells)
        if w is not None:
            return 1 if w == X else -1
        if is_full(board.cells):
            return 0

        return self._minimax(board.cells, depth=len(board.history))

    def choose(self, board):
        """minimax 的价值以 X 为准，X 想要大、O 想要小。"""
        self.stats.reset()
        if winner(board.cells) is not None or is_full(board.cells):
            return None, None
        me = board.current_player
        moves = self.ordering(board.legal_moves())
        scored = []
        for move in moves:
            board.push(move)
            v = self._minimax(board.cells, depth=1)
            board.pop()
            scored.append((v, move))

        if not scored:
            return None, None
        if me == X:
            best = max(v for v, _ in scored)
        else:
            best = min(v for v, _ in scored)
        return random.choice([m for v, m in scored if v == best]), best

    def _minimax(self, cells, depth):
        self.stats.nodes += 1
        w = winner(cells)
        if w is not None:
            self.stats.leaves += 1
            return 1 if w == X else -1
        if is_full(cells):
            self.stats.leaves += 1
            return 0

        if depth % 2 == 0:                     # X 走
            best = -2
            for i in range(N_CELLS):
                if cells[i] == EMPTY:
                    cells[i] = X
                    best = max(best, self._minimax(cells, depth + 1))
                    cells[i] = EMPTY
            return best
        else:                                  # O 走
            best = 2
            for i in range(N_CELLS):
                if cells[i] == EMPTY:
                    cells[i] = O
                    best = min(best, self._minimax(cells, depth + 1))
                    cells[i] = EMPTY
            return best


# ----------------------------------------------------------------------
# 2. negamax（同一件事，代码砍一半）
# ----------------------------------------------------------------------
class NegamaxAgent(BaseAgent):
    """negamax：**永远取最大**，对手的分数取负。

    核心一行：
        value = max(-negamax(child))

    为什么对？因为"这个局面对我多好"和"对这个局面的对手多好"
    永远差一个负号 —— 零和博弈。
    """

    name = "negamax"

    def _search(self, cells, player, depth, alpha, beta):
        self.stats.nodes += 1

        # ⚠️ 这里多了一行"这个局面本身已经结束了吗"的判断。
        #
        # 为什么不能只靠下面那两行？因为**对手可能在你落子之前就已经赢了**。
        # 递归调用是先落子、再进来，所以"上一手把对手将死"这种情况，
        # 必须在这里拦住 —— 不然我们会一本正经地分析一个早就结束的局面。
        #
        # 这一行是测试逼出来的：`test_minimax_and_negamax_agree_on_every_position`
        # 报出"局面 (1,0,...) 该 O 走：minimax=1 negamax=0" —— 一看就知道
        # negamax 把"X 已经赢了、轮到 O"误判成了平局。
        # **这就是"两套实现必须对上"这类测试的价值：它能抓到单个实现自己测不出来的错。**
        already_won = winner(cells)
        if already_won is not None:
            self.stats.leaves += 1
            return 1 if already_won == player else -1

        if is_full(cells):
            self.stats.leaves += 1
            return 0

        # 正常情况：落子之后才发现终局
        best = -2
        for i in range(N_CELLS):
            if cells[i] == EMPTY:
                cells[i] = player
                value = -self._search(cells, 3 - player, depth + 1, -beta, -alpha)
                cells[i] = EMPTY
                if value > best:
                    best = value
                if best > alpha:
                    alpha = best
                if alpha >= beta:               # 剪枝
                    self.stats.cutoffs += 1
                    break
        return best


# ----------------------------------------------------------------------
# 3. alpha-beta（在 negamax 上加剪枝）—— 本课最终用的
# ----------------------------------------------------------------------
class AlphaBetaAgent(BaseAgent):
    """和 NegamaxAgent 的逻辑**一模一样**，唯一的区别是它会剪枝。

    等一下，那为什么是两个类？
    因为 K2.4 要让你亲眼看到"加了剪枝，节点数少了 30 倍，结果一个不差"。
    把开关做成参数（use_pruning）比写两个类更清楚。
    """

    name = "alphabeta"

    def __init__(self, max_depth=None, ordering=center_corner_edge, use_pruning=True):
        super().__init__(max_depth=max_depth, ordering=ordering)
        self.use_pruning = use_pruning
        if not use_pruning:
            self.name = "negamax(no pruning)"

    def _search(self, cells, player, depth, alpha, beta):
        self.stats.nodes += 1

        # 和 NegamaxAgent 一样，先拦住"这个局面本身已经结束"的情况
        already_won = winner(cells)
        if already_won is not None:
            self.stats.leaves += 1
            return 1 if already_won == player else -1

        if is_full(cells):
            self.stats.leaves += 1
            return 0

        if self.max_depth is not None and depth >= self.max_depth:
            self.stats.evals += 1
            return _eval_to_value(evaluate(cells, player))

        best = -2
        for i in self.ordering([j for j in range(N_CELLS) if cells[j] == EMPTY]):
            cells[i] = player
            value = -self._search(cells, 3 - player, depth + 1, -beta, -alpha)
            cells[i] = EMPTY

            if value > best:
                best = value
            if best > alpha:
                alpha = best
            if self.use_pruning and alpha >= beta:
                self.stats.cutoffs += 1
                break
        return best

    def choose(self, board):
        """覆写一下：把"同分走法"里被剪掉的也算进来会影响随机性，保持简单。"""
        return super().choose(board)


def _eval_to_value(score):
    """把评估函数的实数打分压到 [-0.99, 0.99]，好和"必胜 +1 / 平局 0 / 必败 −1"混用。

    为什么要压？因为"我确信这局赢了"（+1）和"我的评估函数觉得这里不错"（+0.9）
    必须是两回事 —— 前者是**事实**，后者是**猜测**。压缩之后，
    搜索永远优先选真正能赢的走法，只有赢不了时才比较猜测的高低。

    ⚠️ 这个做法很粗糙：它假设**评估函数的打分是线性的、可以跨深度比较**。
    这个假设在真实局面里经常不成立 —— L04 的"概率校准"就是专门讲这个问题的。
    """
    if score > 0.999:
        return 0.99
    if score < -0.999:
        return -0.99
    return max(-0.99, min(0.99, score))


# ----------------------------------------------------------------------
# 4. 陪练：随机对手
# ----------------------------------------------------------------------
class RandomAgent:
    """完全随机的对手。它是我们的第一条"及格线"。"""

    name = "random"

    def choose(self, board):
        moves = board.legal_moves()
        if not moves:
            return None, None
        return random.choice(moves), None
