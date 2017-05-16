from functools import wraps, partial

from .experiment import Experiment


class ExperimentMixin(object):
    """Use Experiment as class mixin.

    Mixin consists of one contextmanager that should wrap original (control) function
    and be called with new (candidate) function.

    Example usage::

        class MyClass(ExperimentMixin):
            def new_func(self, arg, _exp):
                return arg

            @EperimentMixin.experiment(new_func, experiment_arg='_exp')
            def original_func(self, arg, _exp):
                return arg

            @staticmethod
            def _ex_publish(experiment, result):
                context = experiment.get_context()
                Stats().save(context=context, match=result.match)

    .. note:: In order to be able to use decorator, new function should be defined
        before old one

    Extra class attributes mixin would look for (all attributes start with ``_ex_``):

        :_ex_name: Name for this experiment (same as ``Experiment(name='...')``)
        :_ex_context: Experiment-wide context (same as ``Experiment(context=...)``
        :_ex_raise_on_mismatch: same as ``Experiment(raise_on_mismatch=...)``

    Extra attributes that can be passed to ``ExperimentMixin.experiment`` decorator:

        :name: *Control* name
        :context: *Control* context
        :candidate_name: *Candidate* name
        :candidate_context: *Candidate* context
        :experiment_arg: Name of an extra kwarg that will be added to function and will contain
            current ``Experiment`` object. If given, it will be passed to both, control and
            candidate functions.

    .. tip:: It is not always convinient to pass control/candidate context in a decorator
        as it is calculated during compilation, so it's better to use ``experiment_arg``
        and update context directly within control/candidate function.

    Static methods mixin would look for:

        :``_ex_compare(experiment, control, observation)``: same as ``Experiment.compare``
        :``_ex_publish(experiment, result)``: same as ``Experiment.publish``

    """
    @staticmethod
    def experiment(candidate, **kwargs):
        """ Static context manager to wrap control function.

        :param candidate: candidate function
        :param name: Control name (defaults to ``Control``)
        :param context: Control context
        :param candidate_name: Candidate name (defaults to ``Candidate``)
        :param candidate_context: Candidate context
        :param experiment_arg: If given, will pass experiment instance as an extra
            kwarg with given name

        """

        def wrapper(func):
            if not candidate:
                return func

            @wraps(func)
            def subwrapper(self, *func_args, **func_kwargs):
                ex_name = getattr(self, '_ex_name', 'Experiment')
                ex_context = getattr(self, '_ex_context', None)
                raise_on_mismatch = getattr(self, '_ex_raise_on_mismatch', False)
                ex_arg = kwargs.get('experiment_arg', None)

                control_name = kwargs.get('name', 'Control')
                control_context = kwargs.get('context', None)

                candidate_name = kwargs.get('candidate_name', 'Candidate')
                candidate_context = kwargs.get('candidate_context', None)

                experiment = Experiment(
                    name=ex_name,
                    context=ex_context,
                    raise_on_mismatch=raise_on_mismatch)

                if ex_arg:
                    func_kwargs.update({ex_arg: experiment})

                for fname in ['compare', 'publish']:
                    ex_func = getattr(self, '_ex_{fname}'.format(fname=fname), None)
                    if ex_func:
                        setattr(experiment, fname, partial(ex_func, experiment))

                with experiment.control(name=control_name, context=control_context) as c:
                    c.record(func(self, *func_args, **func_kwargs))

                with experiment.candidate(name=candidate_name, context=candidate_context) as c:
                    c.record(candidate(self, *func_args, **func_kwargs))

                return experiment.run()

            return subwrapper
        return wrapper
