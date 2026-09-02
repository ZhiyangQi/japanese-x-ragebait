# Dataset files

## Splits

- `train.csv`: 16,558 examples, balanced between 8,279 ragebait and 8,279 non-ragebait labels.
- `test.csv`: 2,000 examples, balanced between 1,000 ragebait and 1,000 non-ragebait labels.
- `manifest.json`: release state, schema, class counts, file sizes, and SHA-256 checksums.

## Columns

| Column | Values | Notes |
| --- | --- | --- |
| `tweet_id` | Numeric string | X Post ID; retain as a string. |
| `label` | `0`, `1` | `1` denotes ragebait. |
| `label_name` | `NO`, `YES` | Readable equivalent of `label`. |
| `annotation_rounds` | string | Sampling/annotation provenance; multiple values are separated by `\|`. |

## Excluded fields

The source research files contain post text for internal analysis. The release-generation step deliberately excludes that column. The public files also exclude usernames, profiles, URLs, media, and user-level attributes.

Never replace these files with the internal source CSVs. Run `python scripts/validate_release.py` before every public release.

