import mock
import pytest

import laboratory
from laboratory.observation import Observation


def raise_exception():
    return {'a': 'b'}['c']


def test_control_raising_exception():
    experiment = laboratory.Experiment()
    with pytest.raises(KeyError):
        with experiment.control() as e:
            e.record(raise_exception())

    assert experiment._control.failure


def test_candidate_raising_exception_silently():
    experiment = laboratory.Experiment()
    with experiment.control() as e:
        e.record(True)

    with experiment.candidate() as e:
        e.record(raise_exception())

    experiment.conduct()
    assert True


def test_raise_on_mismatch():
    experiment = laboratory.Experiment(raise_on_mismatch=True)
    with experiment.control() as e:
        e.record(42)

    with experiment.candidate() as e:
        e.record(0)

    with pytest.raises(laboratory.exceptions.MismatchException):
        experiment.conduct()

    experiment = laboratory.Experiment(raise_on_mismatch=True)
    with experiment.control() as e:
        e.record(42)

    with experiment.candidate() as e:
        e.record(raise_exception())

    with pytest.raises(laboratory.exceptions.MismatchException):
        experiment.conduct()


@mock.patch.object(laboratory.Experiment, 'publish')
def test_set_context(publish):
    experiment = laboratory.Experiment(context={'ctx': True})

    with experiment.control() as e:
        e.record(0)
        assert e.context == {'ctx': True}

    with experiment.candidate() as e:
        e.record(0)
        e.update_context({'ctx': False})
        assert e.context == {'ctx': False}

    with experiment.candidate(context={'additional': 1}) as e:
        e.record(0)
        assert e.context == {'ctx': True, 'additional': 1}

    assert experiment.get_context() == {'ctx': True}
    assert experiment.conduct() == 0
    assert publish.called
    result = publish.call_args[0][0]

    assert result.control.get_context() == {'ctx': True}
    assert result.observations[0].get_context() == {'ctx': False}
    assert result.observations[1].get_context() == {'ctx': True, 'additional': 1}


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
