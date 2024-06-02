import requests


def exit_on_http_error(fn):
    def inner(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except requests.exceptions.HTTPError:
            exit(1)

    return inner
