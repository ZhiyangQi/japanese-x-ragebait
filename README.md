# Japanese Ragebait Dataset

Official repository for **“From Detection to Characterization: A Large-Scale Study of Ragebait on Japanese X”**, accepted at WI-IAT 2026.

**Paper:** [arXiv:2609.02262](https://arxiv.org/abs/2609.02262)

> **ID-only release:** the release files contain only the X Post IDs used in the study's training and test splits. They contain no per-Post labels, post text, annotation reasons, usernames, profiles, URLs, media, or hydrated X objects.

## What is ragebait?

**Ragebait** is online content deliberately framed to provoke anger or outrage—often through frustrating, inflammatory, or offensive presentation—in order to attract attention, clicks, replies, or other engagement.

Oxford University Press named *rage bait* the **[Oxford Word of the Year 2025](https://corp.oup.com/word-of-the-year/)**, reporting that its usage had tripled over the preceding 12 months. The recognition reflects growing public awareness of how outrage can be deliberately used to capture attention and drive online engagement.

## ID-only dataset

| Split | Post IDs | File |
| --- | ---: | --- |
| Train | 16,558 | [`data/train_ids.csv`](data/train_ids.csv) |
| Test | 2,000 | [`data/test_ids.csv`](data/test_ids.csv) |
| **Total** | **18,558** | |

Each file contains a single `tweet_id` column. The two files identify only which original X Posts were included in the study's training and test datasets.

> **Important:** inclusion in either file does **not** mean that a Post was labeled as ragebait. The original study dataset contained both ragebait and non-ragebait examples, but this repository does not disclose the label assigned to any individual Post.

## Why only Post IDs are included

The current [X Developer Policy](https://docs.x.com/developer-terms/policy) restricts redistribution of hydrated X content in downloadable datasets. The [restricted-use guidance](https://docs.x.com/developer-terms/restricted-use-cases) recommends sharing Post IDs so researchers can request the current public object directly from X.

The ID-only format also minimizes disclosure from the research annotations. No label mapping or annotation reason is released. Researchers must obtain currently available objects directly from X through an officially permitted interface using their own credentials. Deleted, protected, suspended, or otherwise unavailable Posts must remain unavailable.

## Schema

| Field | Type | Description |
| --- | --- | --- |
| `tweet_id` | string | X Post ID. Keep as a string to avoid integer precision loss. |

There is deliberately no `label_name` or `reason` field. See [`data/README.md`](data/README.md) for file details.

## Annotation model and prompt

Annotation used OpenAI **GPT-5.4 mini**, with the API model identifier `gpt-5.4-mini`. Requests were submitted through the Chat Completions Batch API with `temperature=0.2`.

A Japanese binary-classification prompt was used. It defines ragebait in terms of intentional provocation and distinguishes it from ordinary negative opinions, complaints, news sharing, and calm criticism.

- [Full Japanese annotation prompt](prompts/ragebait_annotation_ja.txt)
- Output label: `YES` or `NO`
- Prompt role: `user`
- Model: `gpt-5.4-mini`
- Temperature: `0.2`

The internal labels are LLM-generated pseudo-labels rather than manually established gold labels. The accompanying paper reports a separate two-annotator validation on a balanced sample of 200 Posts. The prompt is released for methodological transparency, but its per-Post outputs, including labels and reasons, are not released.

## Intended use and limitations

- Intended for non-commercial academic research, peer review, and validation of the accompanying study.
- Do not interpret inclusion in these files as a ragebait classification or as a factual claim about a Post or its author.
- Do not use this resource to profile, rank, target, identify, harass, surveil, or make consequential decisions about individual users.
- Ragebait is contextual and intent-based. The unreleased research labels may contain annotation errors and should not be treated as facts about a person.
- Post IDs and any content obtained from them remain subject to the current X terms and policies.
- This repository grants no license to X content. See [`DATA_USE.md`](DATA_USE.md).

## Models

The three trained checkpoints and their model cards are publicly available on Hugging Face.

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

For dataset corrections, removal concerns, or reproducibility questions, open a GitHub issue.
