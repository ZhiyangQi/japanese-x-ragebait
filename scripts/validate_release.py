#!/usr/bin/env python3
"""Validate that the public release contains labels and IDs, not X content."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
EXPECTED_FIELDS = ["tweet_id", "label_name"]
FORBIDDEN_FIELDS = {
    "text",
    "tweet_text",
    "post_text",
    "username",
    "screen_name",
    "name",
    "url",
    "profile",
    "author_id",
    "media",
}
EXPECTED = {
    "train": {"rows": 16558, "labels": {"YES": 8279, "NO": 8279}},
    "test": {"rows": 2000, "labels": {"YES": 1000, "NO": 1000}},
}
ID_PATTERN = re.compile(r"^[0-9]{1,19}$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    manifest_path = DATA_DIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    all_ids: set[str] = set()

    for split, expected in EXPECTED.items():
        path = DATA_DIR / f"{split}.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames or []
            if fields != EXPECTED_FIELDS:
                fail(f"{path}: expected fields {EXPECTED_FIELDS}, found {fields}")
            if FORBIDDEN_FIELDS.intersection(field.lower() for field in fields):
                fail(f"{path}: prohibited content field found")

            counts: Counter[str] = Counter()
            split_ids: set[str] = set()
            rows = 0
            for row in reader:
                rows += 1
                post_id = row["tweet_id"]
                if not ID_PATTERN.fullmatch(post_id):
                    fail(f"{path}: invalid Post ID at row {rows + 1}")
                if post_id in split_ids:
                    fail(f"{path}: duplicate Post ID {post_id}")
                split_ids.add(post_id)
                counts[row["label_name"]] += 1
                if row["label_name"] not in {"YES", "NO"}:
                    fail(f"{path}: invalid label at row {rows + 1}")

        if rows != expected["rows"]:
            fail(f"{path}: expected {expected['rows']} rows, found {rows}")
        if dict(counts) != expected["labels"]:
            fail(f"{path}: expected labels {expected['labels']}, found {dict(counts)}")
        overlap = all_ids.intersection(split_ids)
        if overlap:
            fail(f"{path}: {len(overlap)} IDs overlap another split")
        all_ids.update(split_ids)

        manifest_split = manifest["splits"][split]
        if manifest_split["sha256"] != sha256(path):
            fail(f"{path}: checksum does not match manifest")
        print(f"PASS {split}: {rows:,} rows; labels={dict(counts)}")

    if manifest["contains_post_text"] or manifest["contains_user_profiles"]:
        fail("Manifest must declare that content and profiles are absent")
    if manifest["total_rows"] != len(all_ids):
        fail("Manifest total does not match unique Post IDs")

    print(f"PASS release: {len(all_ids):,} unique Post IDs; no prohibited columns")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL {error}", file=sys.stderr)
        raise SystemExit(1)
