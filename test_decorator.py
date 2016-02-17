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

    dummy_control_match("blah")
