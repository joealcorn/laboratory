
class Result(object):

    def __init__(self, experiment, control, observations):
        self.experiment = experiment
        self.control = control
        self.observations = observations

        self.match = all([
            self.experiment.compare(self.control, o)
            for o in self.observations
        ])
