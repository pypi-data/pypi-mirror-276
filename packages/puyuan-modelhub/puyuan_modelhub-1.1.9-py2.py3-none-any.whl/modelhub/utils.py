import pydantic

if pydantic.VERSION < "2.0.0":
    from pydantic import BaseModel
else:
    from pydantic.v1 import BaseModel

import numpy as np


def similarity_np(qe: list[float], pe: list[list[float]]) -> list[float]:
    return np.array(qe) @ np.array(pe).T


def retrieve_top_k(
    passages: list[str],
    query_embedding: list[float],
    passage_embeddings: list[list[float]],
    top_k: int,
    score_threshold: float,
):
    scores = np.mean(similarity_np(query_embedding, passage_embeddings), axis=0)
    idxs = np.argsort(scores)[::-1][:top_k]
    idxs = idxs[scores[idxs] > score_threshold]
    return dict(
        passages=[passages[i] for i in idxs],
        idxs=idxs.tolist(),
        scores=scores[idxs].tolist(),
    )


__all__ = ["BaseModel"]
