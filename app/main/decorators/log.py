import functools


def log_controller_handler(func):
    @functools.wraps(func)
    def wrapper_handler(*args, **kwargs):
        response = func(*args, **kwargs)
        return response

    return wrapper_handler
