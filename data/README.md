# Dataset availability

No row-level dataset files are currently distributed in this repository. The previously staged `train.csv`, `test.csv`, and `manifest.json` files have been withdrawn while the authors complete the appropriate institutional ethics and compliance review.

The study dataset contains 16,558 training examples and 2,000 test examples. Each split is balanced between ragebait and non-ragebait labels. These counts are provided for documentation only and are not a data release.

## Planned columns

| Column | Values | Notes |
| --- | --- | --- |
| `tweet_id` | Numeric string | X Post ID; retain as a string. |
| `label_name` | `NO`, `YES` | `YES` denotes ragebait; `NO` denotes non-ragebait. |

## Planned exclusions

If a future release is approved, it will not include post text, usernames, profiles, direct URLs, media, annotation reasons, hydrated Post objects, or user-level attributes. The final fields, access mechanism, license, and permitted uses may change following institutional review, platform-policy confirmation, and risk assessment.

Do not add source or derived row-level data to this repository unless the required review and release checks have been completed. Run `python scripts/validate_release.py` to confirm that the repository remains in the withheld state.
