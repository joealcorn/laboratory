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

        for observation in self.observations:
            if not self.compare(control.value, observation):
                msg = '%s does not match control value (%s != %s)' % (
                        observation.name, control.value, observation.value
                )
                raise exceptions.MismatchException(msg)

        return value

    def compare(self, control, *candidates):
        return all([
            control == c for c in candidates
        ])

    def publish(self):
        raise NotImplementedError
