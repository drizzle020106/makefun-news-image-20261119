#!/usr/bin/env python3
"""Entry point for the news-image-20261119 bounty.

Standard library only: copies the pre-rendered entry.png (built by
draw.py at build time) into the output directory the grader provides
via MAKEFUN_OUTPUT_DIR. Deterministic by construction -- the same
bytes are copied on every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        sys.stderr.write("MAKEFUN_OUTPUT_DIR is not set\n")
        return 1
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
