from typing import Any, List, Tuple, TypedDict


class ApproxParams(TypedDict):
    guess_min: int
    guess_max: int
    guess_offchain: int
    max_iteration: int
    eps: int
