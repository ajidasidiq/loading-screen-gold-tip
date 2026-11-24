#!/usr/bin/env python3
"""Write the loading-screen tip to /output/entry.txt.

One line, at most 200 characters, aimed at a stressed developer and the
AI coding agent sitting beside them, mid-build.
"""

import os
import sys

TIP = "Tip: this spinner has no idea what is happening either \u2014 you and your agent are just two coworkers staring at the same build, pretending to understand it."

MAX_CHARS = 200


def main() -> int:
    # Gate self-check: one line, within the cap, no control characters.
    if "\n" in TIP or "\r" in TIP:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if not TIP.strip():
        print("error: entry must not be blank", file=sys.stderr)
        return 1
    if len(TIP) > MAX_CHARS:
        print(f"error: entry is {len(TIP)} chars, over the {MAX_CHARS} cap",
              file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 for ch in TIP):
        print("error: entry contains control characters", file=sys.stderr)
        return 1

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(TIP + "\n")

    # Read-back verification: the bytes on disk must be exactly the entry,
    # one line, one trailing newline, nothing else.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != (TIP + "\n").encode("utf-8"):
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    decoded = raw.decode("utf-8")
    if decoded.count("\n") != 1 or decoded.rstrip("\n") != TIP:
        print("error: read-back has extra lines or altered text", file=sys.stderr)
        return 1
    line = decoded.rstrip("\n")
    if line != line.strip():
        print("error: entry has leading or trailing whitespace", file=sys.stderr)
        return 1

    print(f"wrote {len(TIP)}-character entry to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
