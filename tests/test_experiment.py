import mock
import pytest

import laboratory
from laboratory.observation import Observation, unrecorded


class ResultExperiment(laboratory.Experiment):
    def publish(self, result):
        self._result = result

def raise_exception():
    return {'a': 'b'}['c']



def test_experiment_must_contain_control():
    experiment = laboratory.Experiment()
    try:
        experiment.conduct()
    except laboratory.LaboratoryException as ex:
        assert ex.message == 'Your experiment must contain a control case'
    else:
        assert False, 'Expected LaboratoryException to be raised'

def test_experiment_can_not_rerecord_control():
    experiment = laboratory.Experiment()
    experiment.control(lambda: True)
    try:
        experiment.control(lambda: True)
    except laboratory.LaboratoryException as ex:
        assert ex.message == 'You have already established a control case'
    else:
        assert False, 'Expected LaboratoryException to be raised'


def test_control_raising_exception():
    experiment = laboratory.Experiment()
    experiment.control(raise_exception)
    with pytest.raises(KeyError):
        experiment.conduct()


def test_candidate_raising_exception_silently():
    experiment = ResultExperiment()
    experiment.control(lambda: True)
    experiment.candidate(raise_exception)
    experiment.conduct()
    result = experiment._result

    obs = result.candidates[0]
    assert not result.match
    assert obs.value == unrecorded
    assert obs.exception is not None


def test_raise_on_mismatch():
    experiment = laboratory.Experiment(raise_on_mismatch=True)
    experiment.control(lambda: 42)
    experiment.candidate(lambda: 0)

    with pytest.raises(laboratory.exceptions.MismatchException):
        experiment.conduct()

    experiment = laboratory.Experiment(raise_on_mismatch=True)
    experiment.control(lambda: 42)

    experiment.candidate(raise_exception)
    with pytest.raises(laboratory.exceptions.MismatchException):
        experiment.conduct()


@mock.patch.object(laboratory.Experiment, 'publish')
def test_set_context(publish):
    experiment = laboratory.Experiment(context={'ctx': True})
    experiment.control(lambda: 0, context={'control': True})
    experiment.candidate(lambda: 0, context={'ctx': False, 'candidate': True})

    experiment.conduct()
    assert publish.called
    result = publish.call_args[0][0]

    assert experiment.get_context() == {'ctx': True}
    assert result.control.get_context() == {'ctx': True, 'control': True}
    assert result.candidates[0].get_context() == {'ctx': False, 'candidate': True}


def test_repr_without_value():
    obs = Observation("an observation")
    assert repr(obs) == "Observation(name='an observation', value=Unrecorded)"


def test_repr():
    obs = Observation("an observation")
    a_somewhat_complex_value = {'foo': 'bar'}
    obs.record(a_somewhat_complex_value)
    assert repr(obs) == """Observation(name='an observation', value={'foo': 'bar'})"""


def test_repr_with_exception():
    obs = Observation("an observation")
    obs.set_exception(ValueError("something is wrong"))
    assert repr(obs) == """Observation(name='an observation', value=Unrecorded, exception=ValueError('something is wrong',))"""
