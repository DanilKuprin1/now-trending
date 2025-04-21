from time import time

_connection_request_dict: dict[str, float] = {}

_ALLOWED_REQUESTS_PER_SECOND = 1


def is_rate_limited(ip: str) -> bool:
    is_limited = False
    if ip in _connection_request_dict:
        if (time() - _connection_request_dict[ip]) > (1 / _ALLOWED_REQUESTS_PER_SECOND):
            is_limited = False
        else:
            is_limited = True
    _connection_request_dict[ip] = time()
    return is_limited
