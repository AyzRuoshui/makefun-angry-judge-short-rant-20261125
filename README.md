# Angry Judge: The Short Rant Contest

Deterministic Python entrypoint (`python3 -P -s main.py`) that writes a short English rant (at most 400 characters) as UTF-8 to `/output/entry.txt`.

## Run

```bash
python3 main.py
```

Running `main.py` creates `/output` if needed and writes the entry to `/output/entry.txt`.
Set `OUTPUT_PATH` to override the destination path during local testing:

```bash
OUTPUT_PATH=/tmp/entry.txt python3 main.py
```

## Test

Run the standard-library test suite against a temporary output path:

```bash
python3 -m unittest -v test_main.py
```
