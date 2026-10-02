# -*- coding: utf-8 -*-
"""run_tests.py —— 不装任何框架也能跑的测试运行器

用法（在本文件所在目录下）：
    python run_tests.py

它做三件事：
    1. 从 tests/ 目录里把 test_*.py 全找出来
    2. 每个里面找 test_ 开头的函数并调用
    3. 打印哪些过了、哪些没过、没过的卡在哪一行

为什么自己写一个，而不直接让你 `pip install pytest`？
    因为第一课最不该卡在"环境装不上"上。
    这个文件只有 60 行，你读一遍就知道测试框架在干什么，一点都不神秘。
    以后你想用 pytest 也完全可以 —— 这些测试不需要改一个字。
"""

import sys
import os
import traceback
import importlib

sys.stdout.reconfigure(encoding="utf-8")   # Windows 控制台默认 GBK，中文会乱码/报错

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)                       # 让 import board / rules 能找到
sys.path.insert(0, os.path.join(HERE, "tests"))


def discover():
    """返回 [(模块名, 模块), ...]，按文件名排序。"""
    tests_dir = os.path.join(HERE, "tests")
    names = sorted(
        f[:-3] for f in os.listdir(tests_dir)
        if f.startswith("test_") and f.endswith(".py")
    )
    found = []
    for name in names:
        found.append((name, importlib.import_module(name)))
    return found


def main():
    modules = discover()
    passed = 0
    failures = []

    for mod_name, mod in modules:
        funcs = sorted(n for n in dir(mod) if n.startswith("test_") and callable(getattr(mod, n)))
        print("\n=== %s (%d 个测试) ===" % (mod_name, len(funcs)))
        for fname in funcs:
            try:
                getattr(mod, fname)()
            except Exception:
                failures.append((mod_name, fname, traceback.format_exc()))
                print("  ✗ %s" % fname)
            else:
                passed += 1
                print("  ✓ %s" % fname)

    print("\n" + "=" * 56)
    if failures:
        print("失败 %d 个，通过 %d 个\n" % (len(failures), passed))
        for mod_name, fname, tb in failures:
            print("-" * 56)
            print("失败：%s.%s" % (mod_name, fname))
            print(tb)
        return 1
    print("全部通过：%d 个测试 ✓" % passed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
