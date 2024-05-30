from modelhub.types.base import BaseOutput


class RetrieveOutput(BaseOutput):
    passages: list[str]
    idxs: list[int]
    scores: list[float]


class RerankOutput(BaseOutput):
    passages: list[str]
    idxs: list[int]
    scores: list[float]
