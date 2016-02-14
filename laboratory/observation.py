from contextlib import contextmanager
from datetime import datetime


@contextmanager
def Test(observation, raise_exceptions):
    observation.set_start_time()
    try:
        yield observation
    except Exception, ex:
        observation.set_exception(ex)
        if raise_exceptions:
            raise

    finally:
        observation.set_end_time()


class Observation(object):
    def __init__(self, name):
        self.name = name
        self.failure = False
        self.exception = None

    def record(self, value):
        self.value = value

    def set_start_time(self):
        self.start_time = datetime.now()

    def set_end_time(self):
        self.end_time = datetime.now()

    def set_exception(self, exception):
        self.failure = True
        self.exception = exception

    @property
    def duration(self):
        return self.end_time - self.start_time
