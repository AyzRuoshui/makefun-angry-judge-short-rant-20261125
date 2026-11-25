"""Deterministic entry script for the Angry Judge short rant contest."""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_OUTPUT_PATH = Path("/output/entry.txt")
OUTPUT_ENV_VAR = "OUTPUT_PATH"
MAX_CHARACTERS = 400

RANT = (
    "Why install a giant bathroom sink and mount a faucet so short the water "
    "lands half an inch from the back wall? Ninety percent of the bowl sits "
    "bone dry while I scrape my knuckles against the porcelain just to rinse "
    "one thumb. You built a whole basin and forced me to wash my hands in "
    "the margin."
)


def validate_rant(text: str) -> str:
    """Ensure the rant satisfies the contest UTF-8, whitespace, and length rules."""
    if not text.strip():
        raise ValueError("Rant must not be empty or whitespace-only.")
    if text != text.strip():
        raise ValueError("Rant must not have leading or trailing whitespace.")
    if text.startswith("\ufeff") or "\r" in text:
        raise ValueError("Rant must not contain a BOM or carriage returns.")
    try:
        text.encode("utf-8", errors="strict")
    except UnicodeEncodeError as exc:
        raise ValueError("Rant must be valid UTF-8 text.") from exc
    utf16_units = len(text.encode("utf-16-le")) // 2
    if len(text) > MAX_CHARACTERS or utf16_units > MAX_CHARACTERS:
        raise ValueError(f"Rant must be at most {MAX_CHARACTERS} characters.")
    return text


def resolve_output_path() -> Path:
    """Return the target output path, honoring the optional env override."""
    override = os.environ.get(OUTPUT_ENV_VAR, "").strip()
    if override:
        return Path(override)
    return DEFAULT_OUTPUT_PATH


def write_entry(output_path: Path | None = None) -> Path:
    """Write the validated rant as UTF-8 to the output path."""
    validated = validate_rant(RANT)
    target = output_path if output_path is not None else resolve_output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(validated, encoding="utf-8", newline="")
    return target


def main() -> None:
    """CLI entrypoint."""
    write_entry()


if __name__ == "__main__":
    main()
