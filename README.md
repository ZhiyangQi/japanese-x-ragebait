# Japanese Ragebait Dataset

Official repository for **“From Detection to Characterization: A Large-Scale Study of Ragebait on Japanese X”**, accepted at WI-IAT 2026.

> **Review status:** this repository is currently private. The labeled Post ID files are not distributed while the authors complete the appropriate institutional ethics review or obtain a written determination that the release is not subject to review, confirm platform-policy requirements, and finalize the data license and removal process. The authors intend to release the data only after these checks, and only in a reasonable, lawful, and policy-compliant form.

## What is ragebait?

**Ragebait** is online content deliberately framed to provoke anger or outrage—often through frustrating, inflammatory, or offensive presentation—in order to attract attention, clicks, replies, or other engagement. In this project, the term refers specifically to posts whose provocative framing appears intentional; ordinary negative opinions, complaints, news reporting, and calm criticism are not automatically considered ragebait.

Oxford University Press named *rage bait* the **[Oxford Word of the Year 2025](https://corp.oup.com/word-of-the-year/)**, reporting that its usage had tripled over the preceding 12 months. The recognition reflects growing public awareness of how outrage can be deliberately used to capture attention and drive online engagement.

## Planned dataset

| Split | Total | Ragebait | Non-ragebait | Current availability |
| --- | ---: | ---: | ---: | --- |
| Train | 16,558 | 8,279 | 8,279 | Withheld pending review |
| Test | 2,000 | 1,000 | 1,000 | Withheld pending review |
| **Total** | **18,558** | **9,279** | **9,279** | **No row-level files distributed** |

These counts describe the labeled dataset used in the study. This repository currently provides no Post IDs, post text, usernames, user profiles, URLs, media, annotation reasons, or hydrated Post objects.

If a future release is approved, the planned format is **dehydrated** and limited to the minimum fields needed for research validation: Post IDs and `YES`/`NO` research labels. The final access mechanism and scope may change in response to institutional review, X policy, applicable law, and risk assessment.

## Why post text will not be included

The current [X Developer Policy](https://docs.x.com/developer-terms/policy) restricts redistribution of hydrated X content in downloadable datasets. The [restricted-use guidance](https://docs.x.com/developer-terms/restricted-use-cases) recommends sharing Post IDs so researchers can request the current public object directly from X.

Any future release will require researchers to obtain currently available objects directly from X through an officially permitted interface. Deleted, protected, suspended, or otherwise unavailable posts must remain unavailable.

## Planned schema

| Field | Type | Description |
| --- | --- | --- |
| `tweet_id` | string | X Post ID. Keep as a string to avoid integer precision loss. |
| `label_name` | string | `YES` = ragebait, `NO` = non-ragebait. |

See [`data/README.md`](data/README.md) for the planned structure and current review status. No dataset download is currently provided.

## Conditions for a future release

Before distributing row-level data, the authors plan to:

1. Obtain the appropriate institutional ethics review, approval, or written determination of non-applicability.
2. Confirm that the release mechanism and permitted uses comply with the current X terms and policies.
3. Finalize a license for the original research annotations and a clear correction/removal procedure.
4. Reassess re-identification and reputational risks and distribute only the minimum necessary fields.
5. Validate that no post text, usernames, profiles, URLs, media, annotation reasons, or user-level attributes are included.

## Annotation model and prompt

Both GPT-assisted labeling stages used OpenAI **GPT-5.4 mini**, with the API model identifier `gpt-5.4-mini`. Requests were submitted through the Chat Completions Batch API with `temperature=0.2`.

The same Japanese binary-classification prompt was used in both stages. It defines ragebait in terms of intentional provocation and distinguishes it from ordinary negative opinions, complaints, news sharing, and calm criticism.

- [Full Japanese annotation prompt](prompts/ragebait_annotation_ja.txt)
- Output label: `YES` or `NO`
- Prompt role: `user`
- Model: `gpt-5.4-mini`
- Temperature: `0.2`

The labels are LLM-generated pseudo-labels rather than manually established gold labels. The accompanying paper reports a separate two-annotator validation on a balanced sample of 200 posts.

## Repository safeguard

```bash
python scripts/validate_release.py
```

While the data is withheld, the validator fails if row-level CSV files or a release manifest are tracked by Git.

## Intended use and limitations

- Intended for non-commercial academic research, peer review, and validation of the accompanying study.
- Do not use the labels to profile, rank, target, identify, harass, or make consequential decisions about individual users.
- Ragebait is contextual and intent-based. The labels may contain annotation errors and should not be treated as facts about a person.
- Post IDs and any content obtained from them remain subject to the current X terms and policies.
- This repository grants no license to X content. See [`DATA_USE.md`](DATA_USE.md).

## Models

The three trained checkpoints and their model cards are available on Hugging Face. They are currently private during final preparation and are planned for public release.

| Model | Base model | Hugging Face repository |
| --- | --- | --- |
| Rinna RoBERTa | [`rinna/japanese-roberta-base`](https://huggingface.co/rinna/japanese-roberta-base) | [`ZhiyangQi97/japanese-x-ragebait-rinna-roberta-base`](https://huggingface.co/ZhiyangQi97/japanese-x-ragebait-rinna-roberta-base) |
| Tohoku BERT v3 | [`tohoku-nlp/bert-base-japanese-v3`](https://huggingface.co/tohoku-nlp/bert-base-japanese-v3) | [`ZhiyangQi97/japanese-x-ragebait-tohoku-bert-base-v3`](https://huggingface.co/ZhiyangQi97/japanese-x-ragebait-tohoku-bert-base-v3) |
| LINE DistilBERT | [`line-corporation/line-distilbert-base-japanese`](https://huggingface.co/line-corporation/line-distilbert-base-japanese) | [`ZhiyangQi97/japanese-x-ragebait-line-distilbert-base`](https://huggingface.co/ZhiyangQi97/japanese-x-ragebait-line-distilbert-base) |

## Acknowledgments

This work was supported by JST ERATO (JPMJER2502).

## Citation

```bibtex
@inproceedings{qi2026ragebait,
  title     = {From Detection to Characterization: A Large-Scale Study of Ragebait on Japanese X},
  author    = {Qi, Zhiyang and Ito, Kazuhiro and Chen, Jinghui and Nakamura, Hibiki and Chen, Zhangxuan and Murata, Erina and Chujyo, Masaki and Toriumi, Fujio},
  booktitle = {2026 IEEE/WIC International Conference on Web Intelligence and Intelligent Agent Technology (WI-IAT)},
  year      = {2026}
}
```

## Contact

For dataset corrections, removal concerns, or reproducibility questions, open a GitHub issue after the repository is published.
