# chess_ai_tutorial —— 棋类 AI × 传统机器学习

> **目标**：亲手造一个会下棋的 AI，在让它变强的过程中，学会传统机器学习的核心工具。
> **起点**：`教程大纲.md` —— 先读它，那里有 14 课的分课表、每课的知识点清单、三层测验与过关规则。
> **课制**：每课 5–8 小时，若干**强关联知识点**，**每个知识点配一个测验**，全部通过才进下一课。
> **当前状态**：大纲已完成（14 课）；**L01、L02 已生成**（正文 + 代码 + 测试全绿 + 附录 A/C/D/E/F）。
> **下一步**：L02 的答卷在 `notes/测验-L02.md`。L01 你说跳过测验，那就直接从 L02 开始 —— 但 L02 的出关测验里那道核心题（剪枝为什么安全）**必须过**，它是后面 L08 的地基。

---

## 这个目录是什么

这是 `AI学习路线.md` 第 2 步（机器学习）的**项目化落地版**。

和现有文档的关系：

| 文档 | 定位 | 与本目录的关系 |
|---|---|---|
| `../传统机器学习技术栈.md` | 算法词典 / 速查手册 | **本教程的参考书**，遇到不懂的算法去查 |
| `../棋类游戏AI主线.md` | 技术全景图 + 四阶段阶梯 | 本教程的**理论版**，本目录是它的**慢速实操版** |
| `../AI学习路线.md` | 通用 AI 路线（含 LLM/MLOps） | 本教程只取第 2 步，不碰 LLM |
| `../learn_py/` | NumPy / PyTorch 补习 | **并行进行，不冲突**；L13 会用到 |
| `../ANN入门文档.md` | 神经网络入门 | L13 的前置 |

---

## 目录结构

```
chess_ai_tutorial/
├── README.md        ← 你正在看的：导航 + 环境速查
├── 教程大纲.md       ← 【先读这个】14 课分课表、知识点清单、三层测验与过关规则
├── docs/            ← 每课正文 + 附录
│   ├── L01-棋盘规则与测试.md          ← ✅ 已生成
│   ├── L02-搜索minimax与alpha-beta.md ← ✅ 已生成
│   ├── 附录A-Python与NumPy急救包.md   ← ✅
│   ├── 附录C-中英术语对照表.md         ← ✅
│   ├── 附录D-环境与命令速查.md         ← ✅
│   ├── 附录E-进度总表.md              ← ✅ 14 课 × 83 知识点打勾清单
│   └── 附录F-测验答卷模板.md           ← ✅
├── src/             ← 代码，按课分目录
│   ├── part1_tictactoe/   ← ✅ L01：棋盘、规则、31 个测试
│   └── part2_search/      ← ✅ L02：三种搜索算法、对战平台、24 个测试
└── notes/           ← 你的笔记、实验报告、测验答卷
    ├── 测验-L01.md  ← ✅（你说跳过）
    └── 测验-L02.md  ← ✅ 已生成，等填
```

### `src/part2_search/` 里有什么

| 文件 | 作用 |
|---|---|
| `engine.py` | 三个搜索智能体：`MinimaxAgent` / `NegamaxAgent` / `AlphaBetaAgent` + `RandomAgent` |
| `eval_functions.py` | 手工评估函数（K2.6 的主角，也是 L03 的靶子） |
| `arena.py` | 对战平台：`match()` 统计胜率，**自动换边** |
| `main.py` | **和 AI 下棋**（`--depth N` / `--first` / `--random`） |
| `measure.py` | 本课所有实测数字的来源（穷举、节点数、深度爆炸量级） |
| `run_tests.py` | 测试运行器（24 个测试，重点是"剪枝后答案必须一模一样"） |
| `_paths.py` | 把 part1 加进模块搜索路径，让 part2 复用棋盘和规则 |

### `src/part1_tictactoe/` 里有什么

| 文件 | 作用 |
|---|---|
| `constants.py` | `EMPTY` / `X` / `O` / 8 条连线 |
| `board.py` | 棋盘（一维列表 + 落子历史）、坐标换算 |
| `rules.py` | 胜负 / 平局判定、`parse("XXX/.../...")` 测试工具 |
| `main.py` | **命令行双人对下** |
| `buggy.py` | 出关测验：有 3 个 bug 的版本，等你用测试抓出来 |
| `run_tests.py` | 简易测试运行器（不用装 pytest） |
| `tests/` | 31 个测试（`test_board.py` 13 个 + `test_rules.py` 18 个） |
| `verify_buggy.py` | `buggy.py` 的体检报告（卡住了才看） |

---

## 课制速览

| | 说明 |
|---|---|
| **一课** | 5–8 小时（1–2 天），一组"必须一起学才有意义"的知识点 |
| **知识点** | 每课 5–7 个，每个末尾紧跟 2–3 题小测，**即时反馈、可随时中断** |
| **过关** | 全部知识点测验 ✅ + 出关测验 ✅ → 进下一课。允许无限次补考，不允许跳过 |
| **回顾测验** | 每课开头 3 题考上一课，不拦路，但记录在案 |
| **核心主线** | L01–L10（约 65 小时，3 个月）→ 走到 L10 结束即通关 🏁 |
| **延伸** | L11–L14（约 26 小时，选做） |

**为什么是大课而不是小课**：孤立的知识点学不透，因为你不知道它在解决什么、和旁边的怎么配合。划分依据是**耦合强度**，不是内容多少。详见 `教程大纲.md` §0.1。

---

## 环境速查（你这台机器的实际情况）

**结论：`python` 裸命令已经指向 pymanager 装的 Python 3.14.7，直接用它就行。**

```
executable : C:\Users\moon side\AppData\Local\Python\pythoncore-3.14-64\python.exe
version    : 3.14.7
site-packages : 可写 ✅
```

| 操作 | 命令 |
|---|---|
| **跑 L01 的测试** | `cd src\part1_tictactoe` 然后 `python run_tests.py` |
| **下棋** | `cd src\part1_tictactoe` 然后 `python main.py` |
| 跑脚本 | `python src\part1_tictactoe\main.py` |
| 装包 | `python -m pip install --user <包名>` |
| 显式指定版本（保险写法） | `pymanager exec -V:3.14 <脚本.py>` / `pymanager exec -V:3.14 -m pip install <包>` |
| 看已装 | `python -m pip list` |

> ⚠️ **先 `cd` 到代码目录再跑。** `main.py` 里写着 `from board import Board`，Python 只会在"脚本所在目录"和系统目录里找模块。看到 `ModuleNotFoundError`，第一反应就是"我在哪个目录"。

### 已装 / 待装

| 包 | 状态 |
|---|---|
| numpy 2.5.3、matplotlib 3.11.2、torch 2.14.0+cu132、pillow | ✅ 已装 |
| **scikit-learn 1.9.1、pandas 3.0.6、scipy 1.18.1** | ✅ **已装好**（L03 起要用） |

验证一下：

```powershell
python -c "import sklearn, pandas; print('sklearn', sklearn.__version__, '| pandas', pandas.__version__)"
```

> **以后要是还需要装包**，用 `python -m pip install --user <包名>`。
> ⚠️ pip 必须往系统临时目录写解包文件，在受限沙箱里会报 `Permission denied` —— **在你自己的终端里跑就没问题**。这是环境限制，不是你做错了什么。

### 两个已知的坑（写代码时会遇到）

**1. Windows 控制台默认 GBK，打印中文可能报错。** 脚本开头加：

```python
import sys
sys.stdout.reconfigure(encoding="utf-8")
```

**2. 代理端口会变**（装包失败时先查这个）：

```powershell
foreach ($p in @(7897, 10808, 7890)) { "$p : $(Test-NetConnection 127.0.0.1 -Port $p -InformationLevel Quiet)" }
```

---

## 现在怎么开始

**L02 已经准备好了**（L01 的测验按你的意思跳过）。三步：

```powershell
# 1. 先跑一遍测试，确认环境没问题（应该看到「全部通过：24 个测试 ✓」）
cd D:\lg\else\ai_learning\chess_ai_tutorial\src\part2_search
python run_tests.py

# 2. 和 AI 下几局，感受四种强度
python main.py              # 完美 AI（搜到终局）
python main.py --depth 2    # 限深 2 层 + 手工评估
python main.py --depth 1    # 限深 1 层（这个你能赢）
python main.py --random     # 随机对手

# 3. 打开正文，从 K2.1 开始
#    docs\L02-搜索minimax与alpha-beta.md
```

答案写在 `notes\测验-L02.md`（或者直接贴进对话）。**其中出关测验的核心题必须过**：

> alpha-beta 剪掉的分支里，会不会藏着更好的走法？为什么不会？

过了就说一声，我生成 L03。

**当前待确认的三个可选项**（不回答就用默认值）：

1. 主线棋种：**五子棋**（默认）/ 黑白棋 / 四子棋 / 中国象棋
   —— L01–L02 用井字棋热身，从 **L03** 开始就用它了
2. 每周可投入时间 —— 决定我在课内标注的"建议中断点"
3. 数学：**按需给**（默认，讲到"梯度指向增长最快的方向"这个程度）/ 想先集中补一次（附录 B）
