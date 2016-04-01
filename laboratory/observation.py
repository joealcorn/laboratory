from contextlib import contextmanager
from datetime import datetime
import sys


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

class _Unrecorded(object):
    def __repr__(self):
        return "Unrecorded"

unrecorded = _Unrecorded()


class Observation(object):
    def __init__(self, name, context=None):
        self.name = name
        self.failure = False
        self.exception = None
        self.exc_info = None
        self.context = context or {}
        self.value = unrecorded

    def record(self, value):
        self.value = value

    def set_start_time(self):
        self.start_time = datetime.now()

    def set_end_time(self):
        self.end_time = datetime.now()

    def set_exception(self, exception):
        self.failure = True
        self.exception = exception
        self.exc_info = sys.exc_info()

    def get_context(self):
        return self.context

    def update_context(self, context):
        self.context.update(context)

    @property
    def duration(self):
        return self.end_time - self.start_time

    def __repr__(self):
        repr = "Observation(name={name!r}".format(name=self.name)
        repr += ", value={value!r}".format(value=self.value)
        if self.exception:
            repr += ", exception={exception!r}".format(exception=self.exception)
        repr += ")"
        return repr
