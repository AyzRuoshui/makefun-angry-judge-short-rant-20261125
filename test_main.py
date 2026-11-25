"""Standard-library tests for the short rant contest entrypoint."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import main

REPO_ROOT = Path(__file__).resolve().parent
MAIN_SCRIPT = REPO_ROOT / "main.py"


class EntryTest(unittest.TestCase):
    """Verify output path resolution, UTF-8 encoding, and entry limits."""

    def test_default_output_path_without_override(self) -> None:
        previous = os.environ.pop(main.OUTPUT_ENV_VAR, None)
        try:
            self.assertEqual(main.resolve_output_path(), Path("/output/entry.txt"))
            os.environ[main.OUTPUT_ENV_VAR] = "   "
            self.assertEqual(main.resolve_output_path(), Path("/output/entry.txt"))
        finally:
            if previous is not None:
                os.environ[main.OUTPUT_ENV_VAR] = previous
            else:
                os.environ.pop(main.OUTPUT_ENV_VAR, None)

    def test_validate_rant_rules(self) -> None:
        self.assertEqual(main.validate_rant("Valid rant."), "Valid rant.")
        for bad in ("", "   \n\t ", " leading", "trailing ", "\r", "\ufeffhi", "\ud800", "x" * 401):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    main.validate_rant(bad)

    def test_write_entry_creates_nested_parent_and_writes_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "a" / "b" / "entry.txt"
            written = main.write_entry(target)
            self.assertEqual(written, target)
            self.assertEqual(target.read_text(encoding="utf-8"), main.RANT)

    def test_cli_writes_valid_deterministic_utf8_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_root = Path(tmpdir) / "nested" / "output"
            target = out_root / "entry.txt"
            env = os.environ.copy()
            env[main.OUTPUT_ENV_VAR] = str(target)
            env.update({"TZ": "UTC", "PYTHONHASHSEED": "0", "LANG": "C.UTF-8"})

            first = subprocess.run(
                [sys.executable, "-P", "-s", str(MAIN_SCRIPT)],
                cwd=tmpdir,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(first.stdout, "")
            self.assertEqual(first.stderr, "")
            first_bytes = target.read_bytes()

            subprocess.run(
                [sys.executable, "-P", "-s", str(MAIN_SCRIPT)],
                cwd=tmpdir,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            second_bytes = target.read_bytes()

            self.assertEqual(first_bytes, second_bytes)
            self.assertEqual([p.name for p in out_root.iterdir()], ["entry.txt"])
            self.assertFalse(first_bytes.startswith(b"\xef\xbb\xbf"))

            text = first_bytes.decode("utf-8", errors="strict")
            self.assertEqual(text, main.RANT)
            self.assertTrue(text.strip())
            self.assertGreaterEqual(len(text), 1)
            self.assertLessEqual(len(text), main.MAX_CHARACTERS)
            self.assertLessEqual(
                len(text.encode("utf-16-le")) // 2,
                main.MAX_CHARACTERS,
            )


if __name__ == "__main__":
    unittest.main()
