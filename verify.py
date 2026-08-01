"""Syntax check helper: python verify.py <file.py> ..."""
import ast
import sys

for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as fh:
        ast.parse(fh.read())
    print("OK:", path)
