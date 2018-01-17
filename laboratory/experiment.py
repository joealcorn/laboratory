from copy import deepcopy
from functools import wraps
import logging
import traceback
import warnings

from laboratory import exceptions
from laboratory.observation import Observation
from laboratory.result import Result


logger = logging.getLogger(__name__)


class Experiment(object):

    def __init__(self, name='Experiment', context=None, raise_on_mismatch=False):
        self.name = name
        self.context = context or {}
        self.raise_on_mismatch = raise_on_mismatch

        self._control = None
        self._observations = []
        self._candidates = []

    def control(self, control_func, args=None, kwargs=None, name='Control', context=None):
        if self._control is not None:
            raise exceptions.LaboratoryException(
                'You have already established a control case'
            )

        self._control = {
            'func': control_func,
            'args': args or [],
            'kwargs': kwargs or {},
            'name': name,
            'context': context or {},
        }

    def candidate(self, cand_func, args=None, kwargs=None, name='Candidate', context=None):
        self._candidates.append({
            'func': cand_func,
            'args': args or [],
            'kwargs': kwargs or {},
            'name': name,
            'context': context or {},
        })

    def conduct(self):
        if self._control is None:
            raise exceptions.LaboratoryException(
                'Your experiment must contain a control case'
            )

        # Run the control block and then any candidates
        control = self._run_tested_func(raise_on_exception=True, **self._control)
        candidates = [self._run_tested_func(
            raise_on_exception=False, **cand
        ) for cand in self._candidates]

        result = Result(self, control, candidates)

        try:
            self.publish(result)
        except Exception:
            msg = 'Exception occured when publishing %s experiment data'
            logger.exception(msg % self.name)

        return control.value

    def _run_tested_func(self, func, args, kwargs, name, context, raise_on_exception):
        ctx = deepcopy(self.context)
        ctx.update(context)

        obs = Observation(name, ctx)
        self._observations.append(obs)

        obs.set_start_time()
        try:
            obs.record(func(*args, **kwargs))
        except Exception as ex:
            obs.set_exception(ex)
            if raise_on_exception:
                raise
        finally:
            obs.set_end_time()

        return obs

    def run(self):
        warnings.warn('run() is deprecated and will be removed in 1.0. Use conduct() instead', DeprecationWarning)
        return self.conduct()

    def compare(self, control, observation):
        if observation.failure or control.value != observation.value:
            return self._handle_comparison_mismatch(control, observation)

        return True

    def _handle_comparison_mismatch(self, control, observation):
        if self.raise_on_mismatch:
            if observation.failure:
                tb = ''.join(traceback.format_exception(*observation.exc_info))
                msg = '%s raised an exception:\n%s' % (observation.name, tb)
            else:
                msg = '%s does not match control value (%s != %s)' % (
                    observation.name, control.value, observation.value
                )
            raise exceptions.MismatchException(msg)

        return False

    def publish(self, result):
        return

    def get_context(self):
        return self.context

    def _reset_state(self):
        self._control = None
        self._observations = []

    @classmethod
    def decorator(cls, candidate, *exp_args, **exp_kwargs):
        def wrapper(control):
            @wraps(control)
            def inner(*args, **kwargs):
                experiment = cls(*exp_args, **exp_kwargs)
                experiment.control(control, args=args, kwargs=kwargs)
                experiment.candidate(candidate, args=args, kwargs=kwargs)
                return experiment.conduct()
            return inner
        return wrapper
