"""Sentiment analyzer."""

from typing import List, Optional

from sparv import api as sparv_api  # type: ignore [import-untyped]
from transformers import (  # type: ignore [import-untyped]
    AutoModelForSequenceClassification,
    AutoTokenizer,
    MegatronBertForSequenceClassification,
    PreTrainedTokenizerFast,
    pipeline,
)

logger = sparv_api.get_logger(__name__)

TOKENIZER_NAME = "KBLab/megatron-bert-large-swedish-cased-165k"
TOKENIZER_REVISION = "90c57ab49e27b820bd85308a488409dfea25600d"
MODEL_NAME = "KBLab/robust-swedish-sentiment-multiclass"
MODEL_REVISION = "b0ec32dca56aa6182a6955c8f12129bbcbc7fdbd"

TOK_SEP = " "


class SentimentAnalyzer:
    """Sentiment analyzer."""

    def __init__(
        self,
        *,
        tokenizer: Optional[PreTrainedTokenizerFast] = None,
        model: Optional[MegatronBertForSequenceClassification] = None,
        num_decimals: int = 3,
    ) -> None:
        """Create a SentimentAnalyzer using the given tokenizer and model.

        The given number of num_decimals works both as rounding and cut-off.

        Args:
            tokenizer (PreTrainedTokenizerFast): the tokenizer to use
            model (MegatronBertForSequenceClassification): the model to use
            num_decimals (int): number of decimals to use (defaults to 3)
        """
        self.tokenizer = self._default_tokenizer() if tokenizer is None else tokenizer
        self.model = self._default_model() if model is None else model
        self.num_decimals = num_decimals
        self.classifier = pipeline(
            "sentiment-analysis", model=self.model, tokenizer=self.tokenizer
        )

    @classmethod
    def _default_tokenizer(cls) -> PreTrainedTokenizerFast:
        return AutoTokenizer.from_pretrained(TOKENIZER_NAME, revision=TOKENIZER_REVISION)

    @classmethod
    def _default_model(cls) -> MegatronBertForSequenceClassification:
        return AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME, revision=MODEL_REVISION
        )

    @classmethod
    def default(cls) -> "SentimentAnalyzer":
        """Create a SentimentAnalyzer with default tokenizer and model.

        Returns:
            SentimentAnalyzer: the create SentimentAnalyzer
        """
        tokenizer = cls._default_tokenizer()
        model = cls._default_model()
        return cls(model=model, tokenizer=tokenizer)

    def analyze_sentence(self, text: List[str]) -> Optional[str]:
        """Analyze a sentence.

        Args:
            text (Iterable[str]): the text to analyze

        Returns:
            List[Optional[str]]: the sentence annotations.
        """
        sentence = TOK_SEP.join(text)
        classifications = self.classifier(sentence)
        collect_label_and_score = ((clss["label"], clss["score"]) for clss in classifications)
        score_format, score_pred = SCORE_FORMAT_AND_PREDICATE[self.num_decimals]

        format_scores = (
            (label, score_format.format(score)) for label, score in collect_label_and_score
        )
        filter_out_zero_scores = (
            (label, score) for label, score in format_scores if not score_pred(score)
        )
        classification_str = "|".join(
            f"{label}:{score}" for label, score in filter_out_zero_scores
        )
        return f"|{classification_str}|" if classification_str else "|"


SCORE_FORMAT_AND_PREDICATE = {
    1: ("{:.1f}", lambda s: s.startswith("0") and s.endswith(".0")),
    2: ("{:.2f}", lambda s: s.startswith("0") and s.endswith(".00")),
    3: ("{:.3f}", lambda s: s.startswith("0") and s.endswith(".000")),
    4: ("{:.4f}", lambda s: s.startswith("0") and s.endswith(".0000")),
    5: ("{:.5f}", lambda s: s.startswith("0") and s.endswith(".00000")),
    6: ("{:.6f}", lambda s: s.startswith("0") and s.endswith(".000000")),
    7: ("{:.7f}", lambda s: s.startswith("0") and s.endswith(".0000000")),
    8: ("{:.8f}", lambda s: s.startswith("0") and s.endswith(".00000000")),
    9: ("{:.9f}", lambda s: s.startswith("0") and s.endswith(".000000000")),
    10: ("{:.10f}", lambda s: s.startswith("0") and s.endswith(".0000000000")),
}
