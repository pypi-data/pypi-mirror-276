import numpy as np
from um6p_CC_learn.metrics.cosine_similarity import cosine_similarity


def cosine_distances(X, Y=None):
    # Compute cosine similarity
    similarity = cosine_similarity(X, Y)
    # Convert similarity to distances
    distances = 1.0 - similarity
    return distances
