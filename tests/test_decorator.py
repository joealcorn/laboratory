import pytest
import laboratory
from laboratory import ExperimentDecorator


def dummy_candidate_mismatch(x):
    return False


@ExperimentDecorator(candidate=dummy_candidate_mismatch,
                     raise_on_mismatch=True)
def dummy_control_mismatch(x):
    return True


def dummy_candidate_match(x):
    return True


@ExperimentDecorator(candidate=dummy_candidate_match, raise_on_mismatch=True)
def dummy_control_match(x):
    return True


def identity_candidate_match(x):
    return x


@ExperimentDecorator(candidate=identity_candidate_match,
                     raise_on_mismatch=True)
def identity_control_match(x):
    return x


def test_decorated_functions():
    with pytest.raises(laboratory.exceptions.MismatchException):
        dummy_control_mismatch("blah")

    assert dummy_control_match("blah") == True


def test_decorated_observations():
    assert identity_control_match(0) == 0
    assert identity_control_match(1) == 1
