# Japanese Ragebait Dataset

Official dataset release for **“From Detection to Characterization: A Large-Scale Study of Ragebait on Japanese X”**, accepted at WI-IAT 2026.

> **Release candidate:** this repository is prepared for local review and has not yet been published to GitHub.

## Dataset

| Split | Total | Ragebait | Non-ragebait | File |
| --- | ---: | ---: | ---: | --- |
| Train | 16,558 | 8,279 | 8,279 | [`data/train.csv`](data/train.csv) |
| Test | 2,000 | 1,000 | 1,000 | [`data/test.csv`](data/test.csv) |
| **Total** | **18,558** | **9,279** | **9,279** | |

The public files are **dehydrated**: they do not contain post text, usernames, user profiles, URLs, or media. They contain only Post IDs, research labels, and annotation provenance.

## Why the post text is not included

The current [X Developer Policy](https://docs.x.com/developer-terms/policy) restricts redistribution of hydrated X content in downloadable datasets. The [restricted-use guidance](https://docs.x.com/developer-terms/restricted-use-cases) recommends sharing Post IDs so researchers can request the current public object directly from X.

This also means that deleted, protected, suspended, or otherwise unavailable posts remain unavailable when the dataset is used later.

## Schema

| Field | Type | Description |
| --- | --- | --- |
| `tweet_id` | string | X Post ID. Keep as a string to avoid integer precision loss. |
| `label` | integer | `1` = ragebait, `0` = non-ragebait. |
| `label_name` | string | Human-readable label: `YES` or `NO`. |
| `annotation_rounds` | string | Sampling and annotation provenance used during dataset construction. |

See [`data/README.md`](data/README.md) and [`data/manifest.json`](data/manifest.json) for complete release metadata and checksums.

## Load the labels

```python
import pandas as pd

train = pd.read_csv("data/train.csv", dtype={"tweet_id": "string"})
test = pd.read_csv("data/test.csv", dtype={"tweet_id": "string"})

print(train.shape)  # (16558, 4)
print(test.shape)   # (2000, 4)
```

## Rehydrate locally through the official X API

An optional standard-library script looks up up to 100 Post IDs per request using X API v2. It does not request user-profile expansions.

```bash
export X_BEARER_TOKEN="YOUR_TOKEN"

python scripts/rehydrate.py \
  --input data/test.csv \
  --output hydrated/test.jsonl
```

The `hydrated/` directory is excluded from Git. Do not commit or publicly redistribute its contents. API access, availability, pricing, and rate limits are controlled by X and may change.

## Validate the release

```bash
python scripts/validate_release.py
```

The validator checks split sizes, class balance, IDs, headers, duplicate IDs, checksums, and the absence of prohibited content columns.

## Intended use and limitations

- Intended for non-commercial academic research, peer review, and validation of the accompanying study.
- Do not use the labels to profile, rank, target, identify, harass, or make consequential decisions about individual users.
- Ragebait is contextual and intent-based. The labels may contain annotation errors and should not be treated as facts about a person.
- Post IDs and any content obtained from them remain subject to the current X terms and policies.
- This repository grants no license to X content. See [`DATA_USE.md`](DATA_USE.md).

## Models

The trained model checkpoints and model cards will be released separately on Hugging Face. The collection link will be added here after the model release is reviewed.

## Citation

```bibtex
@inproceedings{qi2026ragebait,
  title     = {From Detection to Characterization: A Large-Scale Study of Ragebait on Japanese X},
  author    = {Qi, Zhiyang and Ito, Kazuhiro and Chen, Jinghui and Nakamura, Hibiki and Chen, Zhangxuan and Murata, Erina and Chujyo, Masaki and Toriumi, Fujio},
  booktitle = {WI-IAT 2026},
  year      = {2026}
}
```

## Contact

For dataset corrections, removal concerns, or reproducibility questions, open a GitHub issue after the repository is published.

