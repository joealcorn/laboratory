import pytest

from laboratory.mixin import ExperimentMixin


class MyClassBase(ExperimentMixin):
    should_match = True

    def __init__(self):
        self.new_called = False
        self.old_called = False

    def new_func(self, arg):
        self.new_called = True
        return self.should_match

    @ExperimentMixin.experiment(new_func)
    def old_func(self, arg):
        self.old_called = True
        return True


def test_experiment_mixin():
    obj = MyClassBase()
    assert obj.old_func(1234) is True
    assert obj.old_called is True
    assert obj.new_called is True


def test_publish():
    published = []

    class MyClass(MyClassBase):
        @staticmethod
        def _ex_publish(experiment, result):
            published.append(result)

    MyClass().old_func(123)
    assert len(published) == 1
    result = published[0]
    assert result.match is True


def test_experiment_argument():
    class MyClass(MyClassBase):
        exp = None

        def new_func(self, arg, exp):
            self.new_called = True
            return self.should_match

        @ExperimentMixin.experiment(new_func, experiment_arg='exp')
        def old_func(self, arg, exp):
            self.exp = exp
            self.old_called = True
            return True

    obj = MyClass()
    obj.old_func(123)
    assert obj.exp is not None
