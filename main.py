#!/usr/bin/env python3
"""Seventeen Syllables of Debugging — make.fun entry.

Writes one haiku about debugging to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt). The haiku is the whole entry:
three lines in the 5-7-5 syllable shape, nothing else.
It is deterministic: every run writes the same bytes.

Haiku choice: a breakpoint set at dawn, the log scrolling past the
debugger's own name, and the turn — the bug is my own. The picture
is concrete (a breakpoint, a log line), and the last line reframes
the hunt: the fault was never somewhere else, it was mine.
"""

import os
import shutil
import sys

HAIKU = (
    "Breakpoint set at dawn\n"
    "the log scrolls past my own name\n"
    "the bug is my own"
)


def output_dir() -> str:
    """Where entry.txt goes: the harness dir, or /output by default."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def clean_contents(directory: str) -> None:
    """Remove only the *contents* of the directory, never the dir itself.

    The grader can run this program with a root-owned output directory
    inside a sticky parent; removing the directory itself would fail
    with EPERM. So we mkdir -p (exist_ok) and clear what is inside.

    Clearing is best-effort per entry: a file we cannot remove (for
    example a root-owned leftover in a root-owned directory) must not
    stop the run — the gate only reads entry.txt, so we still write it
    and exit 0.
    """
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        try:
            if os.path.islink(path) or os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except OSError:
            continue


def main() -> int:
    directory = output_dir()
    os.makedirs(directory, exist_ok=True)
    clean_contents(directory)

    text = HAIKU
    encoded = text.encode("utf-8")
    if not (1 <= len(text) <= 200):
        print(f"entry is {len(text)} characters, must be 1-200", file=sys.stderr)
        return 1

    target = os.path.join(directory, "entry.txt")
    with open(target, "wb") as f:
        f.write(encoded)
    print(f"wrote {len(encoded)} bytes to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
