from typing import Any


class EulithAuthException(Exception):
    pass


class EulithRpcException(Exception):
    pass


class EulithUnsafeRequestException(Exception):
    pass


class EulithDeprecationException(Exception):
    pass


class EulithNoSignerException(Exception):
    pass


def guard_non_safe_atomic(ew3: Any) -> None:
    if ew3.is_atomic() and "gnosis_address" not in str(ew3.eulith_service.eulith_url):
        raise EulithUnsafeRequestException(
            "calling this method in an atomic "
            "transaction without a Safe exposes you to "
            "leaving funds in your toolkit contract accidentally"
        )
