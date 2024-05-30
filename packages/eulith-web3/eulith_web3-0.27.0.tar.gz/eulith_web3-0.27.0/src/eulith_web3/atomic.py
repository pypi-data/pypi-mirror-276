from typing import Any, List, Optional, TypedDict


class CommitRequest(TypedDict):
    trace: Optional[bool]
    simulation_type: Optional[str]


class BundleRequest(TypedDict):
    commit_options: Optional[CommitRequest]
    transactions: List[Any]
    auth_address: str
