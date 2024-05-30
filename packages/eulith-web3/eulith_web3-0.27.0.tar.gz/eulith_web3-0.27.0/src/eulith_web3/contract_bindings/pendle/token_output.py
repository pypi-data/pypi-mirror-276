from typing import Any, List, Tuple, TypedDict


class TokenOutput(TypedDict):
    token_out: str
    min_token_out: int
    token_redeem_sy: str
    bulk: str
    pendle_swap: str
    swap_data: Any
