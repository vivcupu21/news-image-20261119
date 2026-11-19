#!/usr/bin/env python3
"""Entrypoint for the news-image-20261119 entry.

The front page is already rendered and stored in this repository as
entry.png. All this program does is copy that file into the directory
the grader names through MAKEFUN_OUTPUT_DIR (or /output when the
variable is not set).

Standard library only. No Pillow, no sibling modules, no network, no
randomness, and nothing is written into the repository itself, so every
run produces byte-identical output.
"""

import hashlib
import os
import shutil
import sys

SIZE_LIMIT = 1_000_000
READ_CHUNK = 1024 * 64


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            block = stream.read(READ_CHUNK)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def _fail(message):
    print(f"main.py: {message}", file=sys.stderr)
    return 1


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(base, "entry.png")
    if not os.path.isfile(source):
        return _fail(f"entry.png missing next to main.py: {source}")

    size = os.path.getsize(source)
    if size >= SIZE_LIMIT:
        return _fail(f"entry.png is {size} bytes, over the {SIZE_LIMIT} byte limit")

    with open(source, "rb") as probe:
        magic = probe.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        return _fail("entry.png does not start with a PNG signature")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, target)

    if os.path.getsize(target) != size:
        return _fail("copied file size differs from entry.png")

    source_hash = _sha256(source)
    copied_hash = _sha256(target)
    if copied_hash != source_hash:
        return _fail("copied file hash differs from entry.png")

    print(f"wrote {target}: {size} bytes, sha256 {copied_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
