from omnia_validation.metrics import (
    compression_ratio,
    normalized_repetition_score,
    shannon_entropy,
)


def test_empty_metrics():
    assert shannon_entropy("") == 0.0
    assert compression_ratio("") == 0.0
    assert normalized_repetition_score("") == 0.0


def test_entropy_repetition_ordering():
    low_entropy = "aaaaaaaaaaaaaaaa"
    high_entropy = "abcdefghijklmnop"

    assert shannon_entropy(low_entropy) < shannon_entropy(high_entropy)
    assert normalized_repetition_score(low_entropy) > normalized_repetition_score(high_entropy)


def test_compression_ratio_repetition_ordering():
    repeated = "abcabcabcabcabcabcabcabc"
    varied = "abcdefghijklmnopqrstuvwx"

    assert compression_ratio(repeated) < compression_ratio(varied)