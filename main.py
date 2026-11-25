"""Deterministic entry script for the Angry Judge short rant contest."""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_OUTPUT_PATH = Path("/output/entry.txt")
OUTPUT_ENV_VAR = "OUTPUT_PATH"
MAX_CHARACTERS = 400

RANT = (
    "A $12 power strip has no business packing a blue LED bright enough to "
    "guide barges through fog. You're charging a phone, not staffing a "
    "lighthouse. Every cheap gadget fires a cobalt pinhole laser built to "
    "pierce closed eyelids at 2 AM. Now I crawl around my bedroom slapping "
    "electrical tape over routers and humidifiers like a cat burglar blinding "
    "sensors, just to darken a room with no lights on."
)


def resolve_output_path() -> Path:
    """Return the target output path, honoring the optional env override."""
    override = os.environ.get(OUTPUT_ENV_VAR, "").strip()
    if override:
        return Path(override)
    return DEFAULT_OUTPUT_PATH


def write_entry(output_path: Path | None = None) -> Path:
    """Write the validated rant as UTF-8 to the output path."""
    if not RANT.strip() or not (1 <= len(RANT) <= MAX_CHARACTERS):
        raise ValueError(
            f"Rant must be 1 to {MAX_CHARACTERS} non-whitespace characters."
        )

    target = output_path if output_path is not None else resolve_output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(RANT, encoding="utf-8", newline="")
    return target


def main() -> None:
    """CLI entrypoint."""
    write_entry()


if __name__ == "__main__":
    main()
