import time
from typing import Union


def rate_limit(max_calls: int, period_seconds: int) -> callable:
    def decorator(func: callable) -> callable:
        calls_history = []

        def wrapper(*args: any, **kwargs: any) -> Union[any, dict]:
            now = time.time()

            calls_history[:] = [t for t in calls_history if t > now - period_seconds]
            if len(calls_history) < max_calls:
                calls_history.append(now)
                result = func(*args, **kwargs)

                return result
            else:
                oldest_call = calls_history[0]
                wait_time = int(period_seconds - (now - oldest_call))
                raise ValueError(f"Too many requests. Retry after {wait_time} seconds.")

        return wrapper

    return decorator


def require_role(required_role: str):
    def real_decorator(func):
        def wrapper(*args, **kwargs):
            user = kwargs.pop("user")
            if user and (
                user.get("role") == required_role or user.get("role") == "admin"
            ):
                return func(*args, **kwargs)
            else:
                raise PermissionError(f"Access denied. Required role: {required_role}")

        return wrapper

    return real_decorator
