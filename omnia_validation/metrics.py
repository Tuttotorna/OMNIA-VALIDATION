"""Small structural metrics used by validation scripts.

These functions are intentionally minimal and semantics-free.
They do not decide correctness.
They only expose simple structural behavior.
"""

from __future__ import annotations

import math
import zlib
from collections import Counter


def shannon_entropy(text: str) -> float:
    """Return Shannon entropy over characters.

    Empty text has entropy 0.0.
    """
    if not text:
        return 0.0

    total = len(text)
    counts = Counter(text)

    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def compression_ratio(text: str, *, encoding: str = "utf-8") -> float:
    """Return compressed_size / raw_size using zlib.

    Lower values usually indicate more repeated structure.
    Empty text has ratio 0.0.
    """
    raw = text.encode(encoding)

    if not raw:
        return 0.0

    compressed = zlib.compress(raw)

    return len(compressed) / len(raw)


def normalized_repetition_score(text: str) -> float:
    """Return a simple normalized repetition score.

    Score range:
        0.0 -> no repeated character mass
        1.0 -> all characters are the same

    This is not a semantic metric.
    """
    if not text:
        return 0.0

    total = len(text)
    counts = Counter(text)
    max_count = max(counts.values())

    if total == 1:
        return 1.0

    return (max_count - 1) / (total - 1)