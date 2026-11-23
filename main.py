#!/usr/bin/env python3
"""Entry point (Python 3.13, standard library only).

Copies the front page this repository holds (entry.png) to the grader's
output directory, mirroring the kit starter (main.ts):

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

The image itself is drawn by render.py (python3 render.py regenerates
entry.png deterministically); this file only delivers the finished bytes,
so both grading runs write identical output.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
print(f"wrote {OUT / 'entry.png'}")
sys.exit(0)
