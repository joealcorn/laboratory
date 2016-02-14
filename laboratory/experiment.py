import logging
import traceback

from laboratory import exceptions
from laboratory.observation import Observation, Test
from laboratory.result import Result

logger = logging.getLogger(__name__)


class Experiment(object):

    def __init__(self, name='Experiment', raise_on_mismatch=False):
        self.name = name
        self.raise_on_mismatch = raise_on_mismatch

        self._control = None
        self._observations = []

    def control(self):
        self._control = Observation('Control')
        return Test(self._control, True)

    def candidate(self, name='Candidate'):
        observation = Observation(name)
        self._observations.append(observation)
        return Test(observation, False)

    def run(self):
        if self._control is None:
            raise exceptions.LaboratoryException(
                'Your experiment must record a control case'
            )

        result = Result(self, self._control, self._observations)

        try:
            self.publish(result)
        except Exception, e:
            msg = 'Exception occured when publishing %s experiment data'
            logger.exception(msg % self.name)

        return self._control.value

    def compare(self, control, *candidates):
        for observation in candidates:
            if observation.failure or control.value != observation.value:
                return self._comparison_mismatch(control, observation)

        return True

    def _comparison_mismatch(self, control, observation):
        if self.raise_on_mismatch:
            if observation.failure:
                msg = '%s raised an exception:\n%s' % (
                    observation.name, traceback.format_exc(observation.exception)
                )
            else:
                msg = '%s does not match control value (%s != %s)' % (
                    observation.name, control.value, observation.value
                )
            raise exceptions.MismatchException(msg)

        return False

    def publish(self, result):
        return
