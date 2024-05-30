"""Sparv plugin for annotating sentences with sentiment analysis."""

from sparv import api as sparv_api  # type: ignore [import-untyped]

from sbx_sentence_sentiment_kb_sent.annotations import annotate_sentence_sentiment
from sbx_sentence_sentiment_kb_sent.constants import PROJECT_NAME

__all__ = ["annotate_sentence_sentiment"]

__description__ = "Annotate sentence with sentiment analysis."
__version__ = "0.1.1"

__config__ = [
    sparv_api.Config(
        f"{PROJECT_NAME}.num_decimals",
        description="The number of decimals to round the score to",
        default=3,
    ),
]
