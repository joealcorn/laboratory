
class Result(object):

    def __init__(self, experiment, control, candidates):
        self.experiment = experiment
        self.control = control
        self.candidates = candidates

        self.match = all([
            self.experiment.compare(self.control, o)
            for o in self.candidates
        ])

    def __repr__(self):
        return "Result(match={}, control={!r}, candidates={!r})".format(
            self.match, self.control, self.candidates
        )
