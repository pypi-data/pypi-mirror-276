# sparv-sbx-sentence-sentiment-kb-sent

[![PyPI version](https://badge.fury.io/py/sparv-sbx-sentence-sentiment-kb-sent.svg)](https://pypi.org/project/sparv-sbx-sentence-sentiment-kb-sent)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sparv-sbx-sentence-sentiment-kb-sent)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/sparv-sbx-sentence-sentiment-kb-sent)](https://pypi.org/project/sparv-sbx-sentence-sentiment-kb-sent/)

[![Maturity badge - level 2](https://img.shields.io/badge/Maturity-Level%202%20--%20First%20Release-yellowgreen.svg)](https://github.com/spraakbanken/getting-started/blob/main/scorecard.md)
[![Stage](https://img.shields.io/pypi/status/sparv-sbx-sentence-sentiment-kb-sent)](https://pypi.org/project/sparv-sbx-sentence-sentiment-kb-sent/)

[![CI(release)](https://github.com/spraakbanken/sparv-sbx-sentiment-analysis/actions/workflows/release-sentence-sentiment-kb-sent.yml/badge.svg)](https://github.com/spraakbanken/sparv-sbx-sentiment-analysis/actions/workflows/release-sentence-sentiment-kb-sent.yml)

Plugin for computing sentence sentiment as a [Sparv](https://github.com/spraakbanken/sparv-pipeline) annotation.

## Install

First, install Sparv as suggested:

```bash
pipx install sparv-pipeline
```

Then install install `sparv-sbx-sentence-sentiment-kb-sent` with

```bash
pipx inject sparv-pipeline sparv-sbx-sentence-sentiment-kb-sent
```

## Usage

Depending on how many explicit exports of annotations you have you can decide to use this
annotation exclusively by adding it as the only annotation to export under `xml_export`:

```yaml
xml_export:
    annotations:
        - <sentence>:sbx_sentence_sentiment_kb_sent.sentence-sentiment--kb-sent
```

To use it together with other annotations you might add it under `export`:

```yaml
export:
    annotations:
        - <sentence>:sbx_sentence_sentiment_kb_sent.sentence-sentiment--kb-sent
        ...
```

### Configuration

You can configure this plugin in the following way.

#### Number of Decimals

The number of decimals defaults to `3` but can be configured in `config.yaml`:

```yaml
sbx_sentence_sentiment_kb_sent:
    num_decimals: 3
```

> [!NOTE] This also controls the cut-off, so all values where the score round to 0.000 (or the number of decimals) is discarded.

### Metadata

#### Model

Type | HuggingFace Model | Revision
--- | --- | ---
Model | [`KBLab/robust-swedish-sentiment-multiclass`](https://huggingface.co/KBLab/robust-swedish-sentiment-multiclass) | b0ec32dca56aa6182a6955c8f12129bbcbc7fdbd
Tokenizer | [`KBLab/megatron-bert-large-swedish-cased-165k`](https://huggingface.co/KBLab/megatron-bert-large-swedish-cased-165k)  | 90c57ab49e27b820bd85308a488409dfea25600d

## Changelog

This project keeps a [changelog](./CHANGELOG.md).
