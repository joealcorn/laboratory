
class Result(object):

    def __init__(self, experiment, control, observations):
        self.experiment = experiment
        self.control = control
        self.observations = observations

        self.match = self.experiment.compare(self.control, *self.observations)
