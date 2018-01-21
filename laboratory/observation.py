from datetime import datetime
import sys


class _Unrecorded(object):
    def __repr__(self):
        return "Unrecorded"


unrecorded = _Unrecorded()


class Observation(object):
    '''
    Result of running a single code block.

    :ivar string name: observation name
    :ivar bool failure: did the function raise an exception
    :ivar Exception exception: exception raised, if any
    :ivar exc_info: result of sys.exc_info(), if exception raised
    :ivar value: function return value
    '''

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

    @property
    def duration(self):
        '''
        How long the function took to execute

        :rtype: timedelta
        '''
        return self.end_time - self.start_time

    def set_exception(self, exception):
        self.failure = True
        self.exception = exception
        self.exc_info = sys.exc_info()

    def get_context(self):
        '''Return observation-specific context'''
        return self.context

    def update_context(self, context):
        self.context.update(context)

    def __repr__(self):
        repr = "Observation(name={name!r}".format(name=self.name)
        repr += ", value={value!r}".format(value=self.value)
        if self.exception:
            repr += ", exception={exception!r}".format(exception=self.exception)
        repr += ")"
        return repr
