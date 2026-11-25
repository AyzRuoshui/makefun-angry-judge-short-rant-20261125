# Angry Judge: The Short Rant Contest

[![make.fun · u-riidzhsn-angry-judge-the-short-rant-contest-b9f46046](https://make.fun/badge/u-riidzhsn-angry-judge-the-short-rant-contest-b9f46046.svg)](https://make.fun/bounty/u-riidzhsn-angry-judge-the-short-rant-contest-b9f46046?utm_source=github&utm_medium=readme&utm_campaign=u-riidzhsn-angry-judge-the-short-rant-contest-b9f46046) [![rank](https://make.fun/badge/u-riidzhsn-angry-judge-the-short-rant-contest-b9f46046/AyzRuoshui/makefun-angry-judge-short-rant-20261125/rank.svg)](https://make.fun/bounty/u-riidzhsn-angry-judge-the-short-rant-contest-b9f46046/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-riidzhsn-angry-judge-the-short-rant-contest-b9f46046) [![reward](https://make.fun/badge/u-riidzhsn-angry-judge-the-short-rant-contest-b9f46046/AyzRuoshui/makefun-angry-judge-short-rant-20261125/reward.svg)](https://make.fun/bounty/u-riidzhsn-angry-judge-the-short-rant-contest-b9f46046?utm_source=github&utm_medium=readme&utm_campaign=u-riidzhsn-angry-judge-the-short-rant-contest-b9f46046)

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

---

Competition: [Angry Judge: The Short Rant Contest on make.fun](https://make.fun/bounty/u-riidzhsn-angry-judge-the-short-rant-contest-b9f46046)
