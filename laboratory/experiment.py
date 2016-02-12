import traceback

from laboratory.observation import Observation, Test
from laboratory import exceptions


class Experiment(object):

    def __init__(self, name='Experiment', raise_on_mismatch=False):
        self.name = name
        self.raise_on_mismatch = raise_on_mismatch

        self._control = None
        self.observations = []

    def control(self):
        self._control = Observation('Control')
        return Test('Control', True, self._control)

    def candidate(self, name='Candidate'):
        observation = Observation(name)
        self.observations.append(observation)
        return Test(name, False, observation)

    def run(self):
        control = self._control
        if control is None:
            raise exceptions.LaboratoryException(
                'Your experiment must record a control case'
            )

        match = self.compare(control, *self.observations)
        self.publish(control, self.observations, match)
        return control.value

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

    def publish(self, control, observations, match):
        return
