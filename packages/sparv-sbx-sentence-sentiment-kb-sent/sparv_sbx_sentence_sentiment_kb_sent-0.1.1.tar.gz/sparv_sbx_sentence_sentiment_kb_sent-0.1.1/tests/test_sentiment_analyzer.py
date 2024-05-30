from typing import Optional

import pytest
from sbx_sentence_sentiment_kb_sent.sentiment_analyzer import SentimentAnalyzer


@pytest.fixture(name="sentiment_analyzer", scope="session")
def fixture_sentiment_analyzer() -> SentimentAnalyzer:
    return SentimentAnalyzer.default()


def test_neutral_text(sentiment_analyzer: SentimentAnalyzer) -> None:
    text = "Vi hoppas och tror att detta också snabbt ska kunna komma på plats , säger Garborg .".split(
        " "
    )

    actual = sentiment_analyzer.analyze_sentence(text)

    actual = remove_scores(actual)
    expected = "|NEUTRAL|"

    assert actual == expected


def remove_scores(actual: Optional[str]) -> Optional[str]:
    """Remove scores."""
    if not actual:
        return actual
    return "|".join(x.split(":")[0] for x in actual.split("|"))
