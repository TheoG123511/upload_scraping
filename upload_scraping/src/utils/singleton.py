import threading


class Singleton(type):

    _instances: dict = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args: tuple, **kwargs: dict) -> isinstance:
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
