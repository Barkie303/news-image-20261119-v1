#!/usr/bin/env python3
"""Entry point for the news-image-20261119 competition.

Copies the front page built by gen.py (entry.png, next to this file)
to the make.fun output directory. Standard library only, no network,
and the same bytes on every run.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = SRC.read_bytes()
    if data[:8] != PNG_MAGIC:
        sys.exit("entry.png does not start with PNG magic bytes")
    dest = out_dir / "entry.png"
    dest.write_bytes(data)
    print(f"wrote {dest} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
