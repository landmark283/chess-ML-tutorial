# -*- coding: utf-8 -*-
"""run_tests.py —— L02 的测试运行器（和 L01 的那个几乎一样）

    cd src/part2_search
    python run_tests.py

唯一的区别：它要先把 `src/part1_tictactoe` 加进模块搜索路径，
因为本课的测试会用到 L01 的 board / rules。
"""

import sys
import os
import traceback
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
PART1 = os.path.join(os.path.dirname(HERE), "part1_tictactoe")
for path in (HERE, PART1, os.path.join(HERE, "tests")):
    if path not in sys.path:
        sys.path.insert(0, path)

sys.stdout.reconfigure(encoding="utf-8")


def discover():
    tests_dir = os.path.join(HERE, "tests")
    names = sorted(
        f[:-3] for f in os.listdir(tests_dir)
        if f.startswith("test_") and f.endswith(".py")
    )
    return [(name, importlib.import_module(name)) for name in names]


def main():
    modules = discover()
    passed = 0
    failures = []

    for mod_name, mod in modules:
        funcs = sorted(n for n in dir(mod)
                       if n.startswith("test_") and callable(getattr(mod, n)))
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
