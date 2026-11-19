"""Entrypoint for the 19 Nov 2026 news-image entry.

Stdlib only: renders the front page through draw_entry and writes entry.png.
Usage: python3 main.py [output-path]
"""

import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIMIT_BYTES = 1_000_000


def main(argv):
    out = Path(argv[1]) if len(argv) > 1 else HERE / "entry.png"
    from draw_entry import render_page

    image = render_page()
    image.save(out, format="PNG")
    data = out.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    print("wrote %s %dx%d %d bytes sha256=%s" % (out, image.width, image.height, len(data), digest))
    if len(data) > LIMIT_BYTES:
        print("WARNING: %s exceeds the %d byte limit" % (out, LIMIT_BYTES))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
