# 附录 A｜Python / NumPy 急救包

> **什么时候看**：遇到语法或库用法卡住时。不用通读 —— 本教程不教 Python 入门，这里只放**在本教程里高频出现、又容易记混**的东西。
> **NumPy 部分**（A.6）在 L03 之前不用管。

---

## A.1 本教程最常用的 10 个 Python 写法

```python
import sys
sys.stdout.reconfigure(encoding="utf-8")     # ← 每个带中文输出的脚本第一行（Windows 必加）

# 1. 列表推导式
squares = [i * i for i in range(5)]                  # [0, 1, 4, 9, 16]
even    = [i for i in range(10) if i % 2 == 0]       # [0, 2, 4, 6, 8]
flat    = [v for row in grid for v in row]           # 摊平二维（双层 for 顺序和嵌套循环一致）

# 2. 生成器表达式：不造列表，省内存
total = sum(v for v in values if v > 0)

# 3. 元组解包
row, col = 1, 2
a, b = b, a                                          # 交换

# 4. divmod：一次拿到商和余数
index = 7
row, col = divmod(index, 3)                          # (2, 1)

# 5. f-string
print(f"第 {i} 手，胜率 {win_rate:.1%}")              # 保留一位小数的百分比

# 6. 字典带默认值
count = {}
count["a"] = count.get("a", 0) + 1
from collections import defaultdict
count = defaultdict(int)
count["a"] += 1                                      # 不用先判断键存不存在

# 7. 同时遍历下标和元素
for i, move in enumerate(moves):
    print(i, move)

# 8. 排序 + 取前 n
top = sorted(items, key=lambda x: -x["score"])[:5]

# 9. 任意长度参数
def mean(*values):
    return sum(values) / len(values)

# 10. 主程序入口 + 防止被 import 时执行
if __name__ == "__main__":
    main()
```

---

## A.2 可变 vs 不可变（L01 的病灶，务必吃透）

| 类型 | 可变？ | 例子 |
|---|---|---|
| `int` / `float` / `bool` / `str` / `tuple` | **不可变** | `1`, `"abc"`, `(1, 2)` |
| `list` / `dict` / `set` / 自定义对象 | **可变** | `[1]`, `{"a": 1}` |

**三条铁律**：

```python
# ① 赋值不是复制 —— 只是多了个名字
a = [1, 2]
b = a
b.append(3)
print(a)          # [1, 2, 3]  ← a 也变了

# ② * n 复制"引用"，不是复制"对象"
bad  = [[0] * 3] * 3          # ❌ 三行是同一个列表
good = [[0] * 3 for _ in range(3)]   # ✅

# ③ 要独立副本就明确说
import copy
shallow = copy.copy(x)        # 只复制最外层容器
deep    = copy.deepcopy(x)    # 里里外外全新
```

**`copy.copy` 的"浅"到底浅在哪**：

```python
x = [[1, 2], [3, 4]]
y = copy.copy(x)
y is x            # False —— 外层列表是新的
y[0] is x[0]      # True  —— 里面那两个列表还是同一批！
y[0][0] = 99
print(x)          # [[99, 2], [3, 4]]  ← 原对象也变了
```

**判断"要不要深拷贝"的一问**：
> 我复制出来的这份东西，会**改动里面装的元素**吗？
> 会 → 深拷贝（或重建）。不会 → 浅拷贝够了。

---

## A.3 `is` vs `==`

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b        # True  —— 值一样
a is b        # False —— 不是同一个对象

c = a
a is c        # True

x = 1000
y = 1000
x is y        # 可能是 False！（小整数有缓存，大整数不一定）
x == y        # True

s1 = "abc"
s2 = "abc"
s1 is s2      # 可能是 True（字符串驻留），但别依赖它
```

**规则**：
- **比"值一样吗"用 `==`**（99% 的场景）
- **比"是不是同一个对象"用 `is`**（通常只和 `None` 用：`if x is None`）
- 在棋盘/搜索代码里，`is` 有用武之地：`shallow.cells is b.cells` 就是靠它揭穿的

---

## A.4 类：本教程会用到的全部程度

```python
class Board:
    def __init__(self):            # 构造：创建对象时自动调用
        self.cells = [0] * 9       # self.xxx = 这个对象自己的数据
        self.history = []

    def push(self, index):         # 普通方法：第一个参数永远是 self
        self.history.append(index)

    @property                      # 只读属性：调用时不用写括号
    def n_moves(self):
        return len(self.history)

    def __len__(self):             # 让 len(board) 能用
        return len(self.history)

    def __str__(self):             # 让 print(board) 好看
        return "\n".join(str(self.cells[i:i+3]) for i in range(0, 9, 3))

b = Board()
b.push(4)
print(b.n_moves)        # 1     ← 注意没有括号
print(len(b))           # 1
```

**几个高频混淆点**：

| 写法 | 含义 |
|---|---|
| `self.n` | **属性**：每个对象一份 |
| `n`（函数内的局部变量） | 函数一结束就没了 |
| `Board.n` | 类属性：所有对象共享（本教程基本不用） |
| `@staticmethod` | 不需要 `self` 的方法 |
| `__init__` | **不是**构造函数，是"初始化"，对象已经存在了才调用它 |

---

## A.5 递归（L02 的主角，先打预防针）

```python
def countdown(n):
    if n == 0:          # ← 递归基：不调用自己的分支
        return
    print(n)
    countdown(n - 1)    # ← 递归步：问题变小
```

**递归三要素**（L02 会反复用）：

1. **递归基**：什么时候直接给答案，不再往下调？
2. **递归步**：怎么把问题变小？
3. **合并**：小问题的答案怎么拼成大问题的答案？

**递归写错的典型症状**：

```
RecursionError: maximum recursion depth exceeded
```

→ 递归基缺失，或者问题没有真的变小（永远到不了递归基）。

**递归为什么适合博弈树**：因为"下棋"天然是递归的 ——
"这个局面的价值 = 我走一步之后，那个局面的价值的反面"。

---

## A.6 NumPy 最小集（L03 之前可以跳过）

```python
import numpy as np

# 造数组
x = np.array([1.0, 2.0, 3.0])
X = np.zeros((3, 4))              # 3 行 4 列全 0
X = np.ones((2, 2))
X = np.arange(9).reshape(3, 3)    # 0..8 摆成 3x3
X = np.random.rand(3, 2)          # [0,1) 均匀随机

# 形状 / 维度（最重要的两个属性）
X.shape      # (3, 4)
X.ndim       # 2
X.size       # 12
X.dtype      # float64

# 索引：切片是"视图"，不是副本！改它会改到原数组
row0  = X[0, :]        # 第 0 行
col1  = X[:, 1]        # 第 1 列
block = X[0:2, 1:3]    # 子块
copy  = X[0, :].copy() # ← 想要独立副本要显式 .copy()

# 布尔索引
X[X > 0.5]             # 挑出所有大于 0.5 的元素（返回一维）
X[X > 0.5] = 0         # 批量赋值

# 广播：形状不同的数组怎么一起算
a = np.array([1, 2, 3])        # shape (3,)
a + 10                          # 标量广播成 (3,)
M = np.zeros((4, 3))
M + a                           # (4,3) + (3,) -> 每一行都加 a

# 常用聚合
X.mean(), X.mean(axis=0), X.mean(axis=1)   # 全局 / 每列 / 每行
X.sum(axis=0)
X.max(), X.argmax()                        # 最大值 / 最大值的位置

# 矩阵乘法（注意和逐元素乘法的区别）
A = np.ones((2, 3)); B = np.ones((3, 4))
A @ B            # (2,4) 矩阵乘法
A * A            # 逐元素相乘（形状必须一致）
```

**三个最容易搞错的点**：

| 坑 | 说明 |
|---|---|
| `axis=0` 还是 `axis=1`？ | `axis=0` = **沿着行方向压缩** = 每列一个结果；`axis=1` = 每行一个结果。记不住就试一次。 |
| 切片是视图 | `b = a[0]` 之后改 `b` 会改到 `a`。这和第 A.2 的浅拷贝是**同一类问题**。 |
| 形状不匹配 | `ValueError: operands could not be broadcast together with shapes (3,) (4,)` —— 看形状，别看值。 |

**为什么机器学习里全用 NumPy**：因为 `for` 循环在 Python 里慢 100 倍。`X.mean(axis=0)` 一行顶你写 20 行循环，而且快得多。L05 讲的数据泄漏、L07 讲的特征缩放，全都建立在这个基础上。

---

## A.7 调试的三个笨办法（但极其有效）

```python
# ① 打印关键中间值（最快，也最容易被忘）
print("legal_moves =", board.legal_moves())
print("type =", type(x), "shape =", getattr(x, "shape", None))

# ② 断言不变量：我"以为"成立的事，写成 assert
assert len(board.cells) == 9, "棋盘长度变成 %d 了" % len(board.cells)
assert board.cells.count(0) + len(board.history) == 9

# ③ 二分法：注释掉一半，看问题还在不在
#    在哪一半消失，问题就在那一半里

# ④ 缩小到最小复现：另开一个 5 行的小脚本重现它
#    —— 这个方法解决 bug 的成功率出乎意料地高
```

**遇到 bug 的四步**（本教程会一直用）：

1. **先复现**：能让它稳定出现吗？
2. **再缩小**：最少需要几行代码才能重现？
3. **提出假设**：我猜是哪一行、为什么？
4. **验证假设**：改一处 / 加一句 print，跑一遍，假设对不对？

> **别做的事**：一次改五个地方然后跑。这样即使好了，你也不知道是哪一处修好的。

---

## A.8 `learn_py/` 与本附录的关系

本教程**不重新教 Python**。如果你的 Python 还觉得虚，`../learn_py/README.md` 那套材料是配套的，可以并行推进，互不冲突：

| `learn_py/` | 本教程 |
|---|---|
| 语言语法、NumPy 索引/广播、PyTorch | **传统**机器学习 + 棋类 AI 工程 |
| 打基础 | 打地基之上盖楼 |

**冲突时以本教程为主**：在真实项目里学的东西记得更牢。哪边不懂就停哪边。
