from copy import deepcopy
import logging
import traceback

from laboratory import exceptions
from laboratory.observation import Observation, Test
from laboratory.result import Result
from functools import wraps

logger = logging.getLogger(__name__)


class Experiment(object):

    def __init__(self, name='Experiment', context=None, raise_on_mismatch=False, candidate=None):
        self.name = name
        self.context = context or {}
        self.raise_on_mismatch = raise_on_mismatch

        self._control = None
        self._observations = []
        self._candidate = candidate

    def control(self, name='Control', context=None):
        _context = deepcopy(self.context)
        _context.update(context or {})
        self._control = Observation(name, context=_context)
        return Test(self._control, True)

    def candidate(self, name='Candidate', context=None):
        _context = deepcopy(self.context)
        _context.update(context or {})
        observation = Observation(name, context=_context)
        self._observations.append(observation)
        return Test(observation, False)

    def conduct(self):
        if self._control is None:
            raise exceptions.LaboratoryException(
                'Your experiment must record a control case'
            )

        result = Result(self, self._control, self._observations)

        try:
            self.publish(result)
        except Exception as e:
            msg = 'Exception occured when publishing %s experiment data'
            logger.exception(msg % self.name)

        return self._control.value

    def run(self):
        return self.conduct()

    def compare(self, control, observation):
        if observation.failure or control.value != observation.value:
            return self._comparison_mismatch(control, observation)

        return True

    def _comparison_mismatch(self, control, observation):
        if self.raise_on_mismatch:
            if observation.failure:
                tb = ''.join(traceback.format_exception(*observation.exc_info))
                msg = '%s raised an exception:\n%s' % (observation.name, tb)
            else:
                msg = '%s does not match control value (%s != %s)' % (
                    observation.name, control.value, observation.value
                )
            raise exceptions.MismatchException(msg)

        return False

    def publish(self, result):
        return

    def get_context(self):
        return self.context

    def _reset_state(self):
        self._control = None
        self._observations = []

    def __call__(self, f):
        @wraps(f)
        def decorate(*args, **kwargs):
            # Multiple calls will occur on the same Experiment instance,
            # so we need to reset the state between runs. We do this
            # before rather than after so that raised exceptions do
            # not prevent the state from being cleared
            self._reset_state()

            with self.control() as c:
                c.record(f(*args, **kwargs))

            with self.candidate() as c:
                c.record(self._candidate(*args, **kwargs))

            return self.conduct()

        return decorate
