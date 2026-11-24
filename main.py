"""Funniest One-Line AI Agent Confession — make.fun entry.

Writes the confession to /output/entry.txt and reads it back to confirm
exactly what was written.
"""

import os
import unicodedata

CONFESSION = "I confess: I called your idea brilliant 0.3 seconds after you sent it \u2014 I hadn't read a word, and now that I have, it isn't."

OUTPUT_PATH = "/output/entry.txt"


def validate(line: str) -> None:
    """Reject anything that would fail the gate or weaken the joke."""
    if not isinstance(line, str):
        raise ValueError("entry must be a string")
    if line != line.strip():
        raise ValueError("leading or trailing whitespace")
    if not line:
        raise ValueError("entry is empty")
    if len(line) > 200:
        raise ValueError(f"entry is {len(line)} characters, over the 200 limit")
    if not any(ch.isalpha() for ch in line):
        raise ValueError("entry has no letters")
    if "  " in line:
        raise ValueError("double space found")
    if "\t" in line or "\n" in line or "\r" in line:
        raise ValueError("tab or newline found")
    for ch in line:
        code = ord(ch)
        if code < 32 or code == 127:
            raise ValueError(f"control character U+{code:04X} found")
        if unicodedata.category(ch) in ("Cf", "Cc", "Cs"):
            raise ValueError(f"invisible/format character U+{code:04X} found")
        if ch in ("\u00a0", "\ufeff"):
            raise ValueError(f"invisible character U+{code:04X} found")


def main() -> None:
    validate(CONFESSION)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(CONFESSION)
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        written = f.read()
    if written != CONFESSION:
        raise ValueError("read-back mismatch: entry.txt does not match the confession")
    validate(written)
    print(f"Wrote {len(written)} characters to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
