#!/usr/bin/env python3
"""Generate single-column ID-only release files from private source CSVs."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID_PATTERN = re.compile(r"^[0-9]{1,19}$")
EXPECTED_ROWS = {"train": 16_558, "test": 2_000}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-source", type=Path, required=True)
    parser.add_argument("--test-source", type=Path, required=True)
    return parser.parse_args()


def read_ids(path: Path, split: str) -> list[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "tweet_id" not in reader.fieldnames:
            raise ValueError(f"{path}: missing tweet_id column")

        post_ids: list[str] = []
        seen: set[str] = set()
        for line_number, row in enumerate(reader, start=2):
            post_id = row["tweet_id"]
            if not ID_PATTERN.fullmatch(post_id):
                raise ValueError(f"{path}:{line_number}: invalid Post ID")
            if post_id in seen:
                raise ValueError(f"{path}:{line_number}: duplicate Post ID")
            seen.add(post_id)
            post_ids.append(post_id)

    expected = EXPECTED_ROWS[split]
    if len(post_ids) != expected:
        raise ValueError(f"{path}: expected {expected:,} IDs, found {len(post_ids):,}")
    return post_ids


def write_ids(path: Path, post_ids: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["tweet_id"])
        writer.writerows([post_id] for post_id in post_ids)


def main() -> int:
    args = parse_args()
    train_ids = read_ids(args.train_source, "train")
    test_ids = read_ids(args.test_source, "test")

    overlap = set(train_ids).intersection(test_ids)
    if overlap:
        raise ValueError(f"train and test contain {len(overlap):,} overlapping IDs")

    write_ids(ROOT / "data/train_ids.csv", train_ids)
    write_ids(ROOT / "data/test_ids.csv", test_ids)
    print(f"Wrote {len(train_ids):,} train IDs and {len(test_ids):,} test IDs; labels excluded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
