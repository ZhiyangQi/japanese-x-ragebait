# ID-only dataset files

This directory contains only the X Post IDs used in the study's training and test splits:

- `train_ids.csv`: 16,558 Post IDs.
- `test_ids.csv`: 2,000 Post IDs.

## Column

| Column | Values | Notes |
| --- | --- | --- |
| `tweet_id` | Numeric string | X Post ID; retain as a string. |

There is no label column. Inclusion in a file means only that the original Post was included in that study split; it does not reveal or imply whether the Post received a ragebait or non-ragebait research label.

## Excluded fields

The files exclude the internal `label_name` and `reason` fields, post text, usernames, profiles, direct URLs, media, hydrated Post objects, and user-level attributes.

Run `python scripts/validate_release.py` before every release. Do not replace these files with internal source CSVs.
