import mock
import pytest
import laboratory
from laboratory import Experiment


def dummy_candidate_mismatch(x):
    return False


@Experiment(candidate=dummy_candidate_mismatch, raise_on_mismatch=True)
def dummy_control_mismatch(x):
    return True


def dummy_candidate_match(x):
    return True


@Experiment(candidate=dummy_candidate_match, raise_on_mismatch=True)
def dummy_control_match(x):
    return True


def test_decorated_functions():
    with pytest.raises(laboratory.exceptions.MismatchException):
        dummy_control_mismatch("blah")

    assert dummy_control_match("blah") == True


def test_observations_reset_with_every_call():
    experiment = Experiment(candidate=lambda value: value)
    @experiment
    def control(value):
        return value

    @experiment
    def control_raises(value):
        raise Exception()

    control(True)
    assert experiment._control.value is True
    assert len(experiment._observations) == 1
    assert experiment._observations[0].value is True

    control(False)
    assert len(experiment._observations) == 1
    assert experiment._control.value is False
    assert experiment._observations[0].value is False

    with pytest.raises(Exception):
        control_raises(False)
    assert len(experiment._observations) == 0
