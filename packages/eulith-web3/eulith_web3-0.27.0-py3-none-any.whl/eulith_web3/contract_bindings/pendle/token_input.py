from typing import Any, List, Tuple, TypedDict


class TokenInput(TypedDict):
    token_in: str
    net_token_in: int
    token_mint_sy: str
    bulk: str
    pendle_swap: str
    swap_data: Any
