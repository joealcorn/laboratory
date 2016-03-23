
class Result(object):

    def __init__(self, experiment, control, observations):
        self.experiment = experiment
        self.control = control
        self.observations = observations

        self.match = all([
            self.experiment.compare(self.control, o)
            for o in self.observations
        ])

    def __repr__(self):
        return "Result(match={}, control={!r}, observations={!r})".format(
            self.match, self.control, self.observations
        )
