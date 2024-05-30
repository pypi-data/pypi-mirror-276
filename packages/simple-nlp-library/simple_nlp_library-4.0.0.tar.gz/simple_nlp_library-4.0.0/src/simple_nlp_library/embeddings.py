import os
from operator import add
from typing import Dict, List


def vectors() -> Dict[str, List[float]]:
    vectors = {}
    file = open(os.path.join(os.path.dirname(__file__), "data/glove.6B.50d.txt"), "r", encoding="utf8")
    for line in file:
        values = line.split()
        key = values[0]
        vector = [float(x) for x in values[1:]]
        vectors[key] = vector
    file.close()
    return vectors


def vectors_average(vectors: List[List[float]]) -> List[float]:
    total = [0.0] * 50
    count = 0
    for vector in vectors:
        total = list(map(add, total, vector))
        count += 1
    if count > 0:
        total = [x / count for x in total]
    return total


def tokens_vector(vectors: Dict[str, List[float]], tokens: List[str]) -> List[float]:
    return vectors_average([vectors[token] for token in tokens if token in vectors])
