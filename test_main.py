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

    def test_cli_writes_valid_deterministic_utf8_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "nested" / "output" / "entry.txt"
            env = os.environ.copy()
            env[main.OUTPUT_ENV_VAR] = str(target)

            subprocess.run(
                [sys.executable, str(MAIN_SCRIPT)],
                cwd=REPO_ROOT,
                env=env,
                check=True,
            )
            first_bytes = target.read_bytes()

            subprocess.run(
                [sys.executable, str(MAIN_SCRIPT)],
                cwd=REPO_ROOT,
                env=env,
                check=True,
            )
            second_bytes = target.read_bytes()

            self.assertEqual(first_bytes, second_bytes)
            self.assertFalse(first_bytes.startswith(b"\xef\xbb\xbf"))

            text = first_bytes.decode("utf-8", errors="strict")
            self.assertEqual(text, main.RANT)
            self.assertTrue(text.strip())
            self.assertGreaterEqual(len(text), 1)
            self.assertLessEqual(len(text), main.MAX_CHARACTERS)


if __name__ == "__main__":
    unittest.main()
