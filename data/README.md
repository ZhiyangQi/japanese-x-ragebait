# Dataset files

## Splits

- `train.csv`: 16,558 examples, balanced between 8,279 ragebait and 8,279 non-ragebait labels.
- `test.csv`: 2,000 examples, balanced between 1,000 ragebait and 1,000 non-ragebait labels.
- `manifest.json`: release state, schema, class counts, file sizes, and SHA-256 checksums.

## Columns

| Column | Values | Notes |
| --- | --- | --- |
| `tweet_id` | Numeric string | X Post ID; retain as a string. |
| `label_name` | `NO`, `YES` | `YES` denotes ragebait; `NO` denotes non-ragebait. |

## Excluded fields

The source research files contain post text and internal annotation metadata. The release-generation step deliberately excludes those columns. The public files also exclude usernames, profiles, URLs, media, and user-level attributes.

Never replace these files with the internal source CSVs. Run `python scripts/validate_release.py` before every public release.
