import functools

from app.infra import LogMongoRepo, get_collection


def log_controller_handler(func):
    @functools.wraps(func)
    def wrapper_handler(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code == 500:
            log_mongo_repo = LogMongoRepo(get_collection("logs"))
            log_mongo_repo.log(response.body["traceback"])
            del response.body["traceback"]

        return response

    return wrapper_handler
