#!/usr/bin/env python3
"""Entry for make.fun's "The Comment Above the Code" bounty.

Writes a single line -- a comment a developer might leave above fragile
production code -- to /output/entry.txt, then verifies the file by reading
it back. The entry must be exactly one line of 1-200 characters.
"""

import sys
from pathlib import Path

ENTRY = "// Removing the sleep below saves 500ms and costs a 3 a.m. page. Your call."
# The line is the whole entry: a warning to the next developer that the
# unexplained sleep is load-bearing, not dead weight.

MAX_LENGTH = 200
OUTPUT_PATH = Path("/output/entry.txt")


def validate_entry(line: str) -> None:
    """Reject anything that is not exactly one short, printable line."""
    if not line:
        raise ValueError("entry is empty")
    if line.strip() == "":
        raise ValueError("entry is only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if len(line) > MAX_LENGTH:
        raise ValueError(
            f"entry is {len(line)} characters, over the {MAX_LENGTH} limit"
        )
    for char in line:
        if ord(char) < 0x20 or ord(char) == 0x7F:
            raise ValueError("entry contains a control character")


def main() -> int:
    validate_entry(ENTRY)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(ENTRY, encoding="utf-8")
    written = OUTPUT_PATH.read_text(encoding="utf-8")
    if written != ENTRY:
        raise ValueError("read-back mismatch: entry.txt differs from entry")
    print(f"wrote {len(ENTRY)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
