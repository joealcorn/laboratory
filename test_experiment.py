import laboratory
import pytest


def raise_exception():
    return {'a': 'b'}['c']


def test_control_raising_exception():
    experiment = laboratory.Experiment()
    with pytest.raises(KeyError):
        with experiment.control() as e:
            e.record(raise_exception())

    assert experiment._control.failure


def test_candidate_raising_exception():
    experiment = laboratory.Experiment()
    with experiment.control() as e:
        e.record(True)

    with experiment.candidate() as e:
        e.record(raise_exception())

    experiment.run()
    assert True


def test_raise_on_mismatch():
    experiment = laboratory.Experiment(raise_on_mismatch=True)
    with experiment.control() as e:
        e.record(42)

    with experiment.candidate() as e:
        e.record(0)

    with pytest.raises(laboratory.exceptions.MismatchException):
        experiment.run()
