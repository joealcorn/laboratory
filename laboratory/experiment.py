from copy import deepcopy
from functools import wraps
import logging
import random
import traceback

from laboratory import exceptions
from laboratory.observation import Observation
from laboratory.result import Result


logger = logging.getLogger(__name__)


class Experiment(object):
    '''
    Experiment base class. Handles running your control and candidate functions.
    Should be subclassed to add publishing functionality.

    :ivar string name: Experiment name
    :ivar dict raise_on_mismatch: Raise :class:`MismatchException` when experiment results do not match
    '''

    def __init__(self, name='Experiment', context=None, raise_on_mismatch=False):
        '''
        :param string name: Experiment name
        :param dict context: Experiment-wide context
        :param bool raise_on_mismatch: Raise if results do not match
        '''

        self.name = name
        self.context = context or {}
        self.raise_on_mismatch = raise_on_mismatch

        self._control = None
        self._candidates = []

    @classmethod
    def decorator(cls, candidate, *exp_args, **exp_kwargs):
        '''
        Decorate a control function in order to conduct an experiment when called.

        :param callable candidate: your candidate function
        :param iterable exp_args: positional arguments passed to :class:`Experiment`
        :param dict exp_kwargs: keyword arguments passed to :class:`Experiment`

        Usage::

            candidate_func = lambda: True

            @Experiment.decorator(candidate_func)
            def control_func():
                return True

        '''
        def wrapper(control):
            @wraps(control)
            def inner(*args, **kwargs):
                experiment = cls(*exp_args, **exp_kwargs)
                experiment.control(control, args=args, kwargs=kwargs)
                experiment.candidate(candidate, args=args, kwargs=kwargs)
                return experiment.conduct()
            return inner
        return wrapper

    def control(self, control_func, args=None, kwargs=None, name='Control', context=None):
        '''
        Set the experiment's control function. Must be set before ``conduct()`` is called.

        :param callable control_func: your control function
        :param iterable args: positional arguments to pass to your function
        :param dict kwargs: keyword arguments to pass to your function
        :param string name: a name for your observation
        :param dict context: observation-specific context

        :raises LaboratoryException: If attempting to set a second control case
        '''
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
        '''
        Adds a candidate function to an experiment. Can be used multiple times for
        multiple candidates.

        :param callable cand_func: your control function
        :param iterable args: positional arguments to pass to your function
        :param dict kwargs: keyword arguments to pass to your function
        :param string name: a name for your observation
        :param dict context: observation-specific context
        '''
        self._candidates.append({
            'func': cand_func,
            'args': args or [],
            'kwargs': kwargs or {},
            'name': name,
            'context': context or {},
        })

    def conduct(self):
        '''
        Run control & candidate functions and return the control's return value.
        ``control()`` must be called first.

        :raise LaboratoryException: when no control case has been set
        :return: Control function's return value
        '''
        if self._control is None:
            raise exceptions.LaboratoryException(
                'Your experiment must contain a control case'
            )


        # execute control and exit if experiment is not enabled
        if not self.enabled():
            control = self._run_tested_func(raise_on_exception=True, **self._control)
            return control.value

        # otherwise, let's wrap an executor around all of our functions and randomise the ordering

        def get_func_executor(obs_def, is_control):
            """A lightweight wrapper around a tested function in order to retrieve state"""
            return lambda *a, **kw: (self._run_tested_func(raise_on_exception=is_control, **obs_def), is_control)

        funcs = [
            get_func_executor(self._control, is_control=True),
        ] + [get_func_executor(cand, is_control=False,) for cand in self._candidates]

        random.shuffle(funcs)

        control = None
        candidates = []

        # go through the randomised list and execute the functions
        for func in funcs:
            observation, is_control = func()
            if is_control:
                control = observation
            else:
                candidates.append(observation)

        result = Result(self, control, candidates)

        try:
            self.publish(result)
        except Exception:
            msg = 'Exception occured when publishing %s experiment data'
            logger.exception(msg % self.name)

        return control.value

    def enabled(self):
        '''
        Enable the experiment? If false candidates will not be executed.

        :rtype: bool
        '''
        return True

    def compare(self, control, candidate):
        '''
        Compares two :class:`Observation` instances.

        :param Observation control: The control block's :class:`Observation`
        :param Observation candidate: A candidate block's :class:`Observation`

        :raises MismatchException: If ``Experiment.raise_on_mismatch`` is True

        :return bool: match?
        '''
        if candidate.failure or control.value != candidate.value:
            return self._handle_comparison_mismatch(control, candidate)

        return True

    def publish(self, result):
        '''
        Publish the results of an experiment.
        This is called after each experiment run.
        Exceptions that occur during publishing will be caught, but logged.

        By default this is a no-op. See :ref:`publishing`.

        :param Result result: The result of an experiment run
        '''
        return

    def get_context(self):
        '''
        :return dict: Experiment-wide context
        '''
        return self.context

    def _run_tested_func(self, func, args, kwargs, name, context, raise_on_exception):
        ctx = deepcopy(self.context)
        ctx.update(context)

        obs = Observation(name, ctx)
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
