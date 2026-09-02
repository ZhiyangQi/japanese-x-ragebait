#!/usr/bin/env python3
"""Rehydrate labeled Post IDs locally through X API v2.

The output contains X content and is intentionally written under an ignored
directory by default. Do not commit or publicly redistribute it.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_URL = "https://api.x.com/2/tweets"
BATCH_SIZE = 100


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Dehydrated CSV file.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("hydrated/posts.jsonl"),
        help="Local JSONL output. Keep it outside version control.",
    )
    parser.add_argument(
        "--bearer-token-env",
        default="X_BEARER_TOKEN",
        help="Environment variable containing the X API Bearer Token.",
    )
    return parser.parse_args()


def chunks(rows: list[dict[str, str]], size: int):
    for index in range(0, len(rows), size):
        yield rows[index : index + size]


def request_posts(batch: list[dict[str, str]], token: str) -> dict:
    params = urllib.parse.urlencode(
        {
            "ids": ",".join(row["tweet_id"] for row in batch),
            "tweet.fields": "created_at,lang",
        }
    )
    request = urllib.request.Request(
        f"{API_URL}?{params}",
        headers={"Authorization": f"Bearer {token}", "User-Agent": "japanese-ragebait-research/1.0"},
    )

    while True:
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code != 429:
                detail = error.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"X API returned HTTP {error.code}: {detail}") from error
            reset_at = int(error.headers.get("x-rate-limit-reset", int(time.time()) + 60))
            delay = max(1, reset_at - int(time.time()) + 1)
            print(f"Rate limited; waiting {delay} seconds.", file=sys.stderr)
            time.sleep(delay)


def main() -> int:
    args = parse_args()
    token = os.environ.get(args.bearer_token_env)
    if not token:
        print(f"Missing Bearer Token in ${args.bearer_token_env}.", file=sys.stderr)
        return 2

    with args.input.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    required = {"tweet_id", "label", "label_name", "annotation_rounds"}
    if not rows or not required.issubset(rows[0]):
        print(f"Input must contain: {', '.join(sorted(required))}", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    found = unavailable = 0

    with args.output.open("w", encoding="utf-8") as output:
        for batch_number, batch in enumerate(chunks(rows, BATCH_SIZE), start=1):
            payload = request_posts(batch, token)
            posts = {post["id"]: post for post in payload.get("data", [])}
            errors = {str(error.get("value")): error for error in payload.get("errors", [])}

            for row in batch:
                post_id = row["tweet_id"]
                post = posts.get(post_id)
                record = {
                    "tweet_id": post_id,
                    "label": int(row["label"]),
                    "label_name": row["label_name"],
                    "annotation_rounds": row["annotation_rounds"],
                    "available": post is not None,
                }
                if post is not None:
                    record["post"] = post
                    found += 1
                else:
                    record["api_error"] = errors.get(post_id, {"detail": "Post unavailable"})
                    unavailable += 1
                output.write(json.dumps(record, ensure_ascii=False) + "\n")

            print(
                f"Batch {batch_number}: {min(batch_number * BATCH_SIZE, len(rows))}/{len(rows)} IDs processed",
                file=sys.stderr,
            )

    print(f"Done: {found} available, {unavailable} unavailable. Output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

