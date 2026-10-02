# 附录 D｜环境与命令速查

> **什么时候看**：每次开电脑准备学的时候。把这一页当"开机检查单"。

---

## D.1 这套环境里到底有什么

| 项 | 值 | 说明 |
|---|---|---|
| Python | **3.14.7** | 命令就是 `python` |
| 路径 | `C:\Users\moon side\AppData\Local\Python\pythoncore-3.14-64\python.exe` | 不用管，`python` 已经指向它 |
| 已装 | `numpy` 2.5.3 | 数值计算（L03 起天天用） |
| 已装 | `matplotlib` 3.11.2 | 画图（L03 起天天用） |
| 已装 | `torch` 2.14.0+cu132、`torchvision`、`pillow` | 深度学习（L13 才用） |
| 已装 | `scikit-learn` 1.9.1、`pandas` 3.0.6、`scipy` 1.18.1 | L03 起天天用；已装好 ✅ |
| 备用 | `py -3.11` | Python 3.11.9，也装了 torch |
| 备用 | `pymanager exec -V:3.14 ...` | 你的个人习惯写法，效果同 `python` |

**日常就用 `python`。** 不要在这上面纠结。

**验一下环境还是好的**：

```powershell
python -V
python -c "import numpy, matplotlib, sklearn, pandas; print('numpy', numpy.__version__, '| matplotlib', matplotlib.__version__, '| sklearn', sklearn.__version__, '| pandas', pandas.__version__)"
```

---

## D.2 每次开工的三行命令

```powershell
cd D:\lg\else\ai_learning\chess_ai_tutorial\src\part1_tictactoe
python run_tests.py
python main.py
```

**L01 之后**，代码目录会变成 `part2_search`、`part3_linear_eval`…… **先 `cd` 到对应目录**。

---

## D.3 最常用的命令

| 目的 | 命令 |
|---|---|
| 看版本 | `python -V` |
| 跑脚本 | `python 脚本名.py` |
| 跑测试（本教程） | `python run_tests.py` |
| 看某个包装没装 | `python -c "import sklearn; print(sklearn.__version__)"` |
| 交互式试代码 | `python -i 脚本名.py`（跑完留在解释器里）或直接 `python` 进 REPL |
| 退出 REPL | `exit()` 或 `Ctrl+Z` 回车（Windows） |
| 中断卡住的程序 | `Ctrl+C` |
| 清屏 | `cls` |
| 看当前目录 | `pwd`（PowerShell 里是 `Get-Location`，但 `pwd` 也能用） |
| 列文件 | `ls` / `dir` |
| 装包 | 见 D.5 |

---

## D.4 三个必知的坑

### 坑 1：中文乱码

**症状**：

```
����
```

或者

```
UnicodeEncodeError: 'gbk' codec can't encode character ...
```

**原因**：Python 输出 UTF-8，Windows 控制台按 GBK 解码。

**解法**：脚本开头加两行：

```python
import sys
sys.stdout.reconfigure(encoding="utf-8")
```

本教程所有带中文输出的脚本都有这两行。**你自己写的新脚本也加上。**

### 坑 2：`ModuleNotFoundError`

**症状**：

```
ModuleNotFoundError: No module named 'board'
```

**原因**：99% 是**当前目录不对**。

**解法**：

```powershell
cd D:\lg\else\ai_learning\chess_ai_tutorial\src\part1_tictactoe
python run_tests.py
```

**排查思路**：Python 找模块时，会看"脚本所在目录"和几个系统目录。所以"从哪个目录跑"决定了能不能 import 到隔壁文件。

### 坑 3：`input()` 报 `EOFError`

**症状**：

```
EOFError: EOF when reading a line
```

**原因**：在**非交互**环境里跑了需要键盘输入的程序（比如把输出重定向、或者在管道里跑）。

**解法**：要交互的程序（如 `main.py`）在终端里手动跑，别塞进管道或批处理。

---

## D.5 装包

```powershell
# 普通安装
python -m pip install 包名

# 装到用户目录（不需要管理员权限，推荐）
python -m pip install --user 包名

# 一次装多个
python -m pip install --user scikit-learn pandas

# 看装了哪些
python -m pip list

# 看某个包的信息
python -m pip show scikit-learn
```

**国内镜像**（你这台机器已经配好了阿里云镜像，一般不用管）：

```powershell
python -m pip install --user -i https://mirrors.aliyun.com/pypi/simple/ 包名
```

**L03 之前需要装好的**：`scikit-learn`、`pandas`（`scipy` 会跟着自动装）。
**✅ 这三样已经在你这台机器上装好了**（2026 年这次会话装的）：

```
scikit-learn 1.9.1 | pandas 3.0.6 | scipy 1.18.1
```

验证：

```powershell
python -c "import sklearn, pandas; print('sklearn', sklearn.__version__, '| pandas', pandas.__version__)"
```

> ⚠️ 如果以后 `pip install` 报 `Permission denied`（写入临时目录失败），就在**你自己的终端**（不是任何受限环境）里跑同一条命令。
> **本项目当前的 pip 必须往系统临时目录写解包文件**，在受限沙箱里一定会失败 —— 这是环境限制，不是你做错了什么。

---

## D.6 代理 / 网络（本机情况）

| 项 | 值 |
|---|---|
| 本机代理 | `127.0.0.1:7897` |
| pip 镜像 | 阿里云（已配置） |
| 已知问题 | 直接 `Invoke-WebRequest` 访问部分 HTTPS 站点会报"基础连接已经关闭"（TLS 被拦截） |

**实践建议**：
- **pip 装包没问题**（走镜像）。
- 浏览器查资料没问题。
- 如果要在脚本里抓网页，TLS 可能会挡；那时我们再说，别在这上面花时间。

---

## D.7 学习时建议开着的东西

```powershell
# 窗口 1：工作目录（跑代码）
cd D:\lg\else\ai_learning\chess_ai_tutorial\src\part1_tictactoe

# 窗口 2（可选）：REPL，随时试一行
python
```

编辑器：VS Code 或 PyCharm 都行。**唯一重要的设置**：

> **把 Tab 键设为"插入空格"（indent using spaces, 4 spaces）。**
> Tab 和空格混用会报 `TabError` / `IndentationError`，而且报错信息非常难懂。

---

## D.8 出问题了怎么办（求助模板）

把下面四件事一起发给我，我基本能直接定位：

```
1. 我在哪个目录跑的：cd ...
2. 我跑的命令：python ...
3. 完整报错（从 Traceback 到最后一行，别截断）
4. 我改过什么（如果改了代码）
```

**不要只发一句"报错了"。** 报错信息里的行号和最后一行的错误类型，是最值钱的线索。
