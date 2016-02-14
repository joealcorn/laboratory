from contextlib import contextmanager
from datetime import datetime


@contextmanager
def Test(observation, raise_exceptions):
    observation.set_start_time()
    try:
        yield observation
    except Exception as ex:
        observation.set_exception(ex)
        if raise_exceptions:
            raise

    finally:
        observation.set_end_time()


class Observation(object):
    def __init__(self, name, context=None):
        self.name = name
        self.failure = False
        self.exception = None
        self.context = context or {}

    def record(self, value):
        self.value = value

    def set_start_time(self):
        self.start_time = datetime.now()

    def set_end_time(self):
        self.end_time = datetime.now()

    def set_exception(self, exception):
        self.failure = True
        self.exception = exception

    def get_context(self):
        return self.context

    def update_context(self, context):
        self.context.update(context)

    @property
    def duration(self):
        return self.end_time - self.start_time
