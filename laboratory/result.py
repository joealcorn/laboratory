
class Result(object):
    '''
    :ivar Experiment experiment: The experiment instance that recorded this Result
    :ivar Observation control: The control observation
    :ivar [Observation] candidates: A list of candidate observations
    :ivar bool match: Whether all candidates match the control case
    '''

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
