from functools import wraps
import time
import inspect
import logging


def log(level):
    def decorator(obj):
        logger = logging.getLogger(obj.__name__)
        if inspect.isclass(obj):
            init_fun = obj.__init__

            @wraps(init_fun)
            def wrapped_init(*args, **kwargs):
                ts = time.time()
                start = time.perf_counter()
                end = time.perf_counter()
                logger.log(
                    level=level,
                    msg=f"ts: {ts} duration: {end - start} name: {obj.__name__} args: {args}{kwargs}",
                )

            obj.__init__ = wrapped_init
            return obj
        elif inspect.isfunction(obj):

            @wraps(obj)
            def wrapper(*args, **kwargs):
                ts = time.time()
                start = time.perf_counter()
                obj(*args, **kwargs)
                end = time.perf_counter()
                logger.log(
                    level=level,
                    msg=f"ts: {ts} duration: {end - start} name: {obj.__name__} args: {args}{kwargs} annot: {obj.__annotations__} ",
                )

            return wrapper
        else:
            return obj

    return decorator


if __name__ == "__main__":

    @log(logging.WARNING)
    def test_func(name: str) -> None:
        print(name)

    @log(logging.WARNING)
    class test_cls:
        def __init__(self, name):
            self.name = name

    test_func(name="Siema")
    my_cls = test_cls("Siema")
