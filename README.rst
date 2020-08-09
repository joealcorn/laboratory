Laboratory!
===========

.. image:: https://img.shields.io/travis/joealcorn/laboratory.svg?
    :target: https://travis-ci.org/joealcorn/laboratory

.. image:: https://readthedocs.org/projects/laboratory-python/badge/?version=latest
    :target: https://laboratory-python.readthedocs.io/en/latest/

.. image:: https://img.shields.io/github/license/joealcorn/laboratory.svg?
    :target: https://opensource.org/licenses/mit-license.php

.. image:: https://img.shields.io/pypi/v/laboratory.svg?
    :target: https://pypi.python.org/pypi/laboratory

.. image:: https://pypi-badges.global.ssl.fastly.net/svg?package=laboratory&timeframe=monthly
    :target: https://pypi.joealcorn.co.uk


A Python library for carefully refactoring critical paths by testing in
production (inspired by `GitHub's Scientist`_) with support for Python 2.7, 3.3+

.. _GitHub's Scientist: https://github.com/github/scientist


#. `Why?`_
#. `Installation`_
#. `Getting started`_
#. `Adding context`_
#. `Ramping up`_
#. `Controlling comparison`_
#. `Raise on mismatch`_
#. `Publishing results`_
#. `Caveats`_
#. `Links`_

.. _Why?:

Why?
----

Some blocks of code are more critical than the rest. Laboratory helps us refactor important
code paths by running experiments in production and verifying the results.

The value lies in its ability to give us a sense of confidence where there was none before.
Through experimentation we immediately see if candidate code is misbehaving, and at the same
time we establish a feedback loop that we can use to converge on correctness more quickly.

I've written a blog post if you'd like to know more: `Sure-footed refactoring`_.
The original blog post that inspired this project is worth a read too: `Scientist`_.

.. _Sure-footed refactoring: https://joealcorn.co.uk/blog/2018/sure-footed-refactoring
.. _Scientist: https://githubengineering.com/scientist/


Installation
------------

Installing from pypi is recommended

.. code::

    $ pip install laboratory

You can also install a `tagged version`_ from Github

.. code::

    $ pip install https://github.com/joealcorn/laboratory/archive/v1.0.tar.gz

Or the latest development version

.. code::

    $ pip install git+https://github.com/joealcorn/laboratory.git


.. _tagged version: https://github.com/joealcorn/laboratory/releases

.. _Getting started:

Getting started
---------------

See: `Installation`_ or ``pip install laboratory``

With Laboratory you conduct an experiment with your known-good code as the
control block and a new code branch as a candidate. Laboratory will:

-  Execute the new and the old code in a randomised order
-  Compare the return values
-  Record timing information about old & new code
-  Catch (but record!) exceptions in the new code
-  Publish all of this information

Let's imagine you're refactoring some authorisation code. Your existing code
is working, but it's a fragile pile of spaghetti that is becoming hard to
maintain. You want to refactor, but this is important code and you simply can't
afford to get this wrong or else you risk exposing user data.
Considering the state of the original code, this could be difficult to pull off,
but Laboratory is here to help.

Laboratory helps us verify the correctness of our implementation even with the
cornucopia of factors that make production a unique environment (bad or legacy
data, heavy load, etc.)

Let's set up an experiment to run our old (control) and new (candidate) code:

.. code:: python

    import laboratory

    # set up the experiment and define control and candidate functions
    experiment = laboratory.Experiment()
    experiment.control(authorise_control, args=[user], kwargs={'action': action})
    experiment.candidate(authorise_candidate, args=[user], kwargs={'action': action})

    # conduct the experiment and return the control value
    authorised = experiment.conduct()


Note that the ``Experiment`` class can also be used as a decorator if the
control and candidate functions take the same arguments.

.. code:: python

    def authorise_candidate(user, action=None):
        return True

    @Experiment.decorator(candidate=authorise_candidate)
    def authorise_control(user, action=None):
        return True


An experiment will always return the value of the control block.


Adding context
--------------

A lot of the time there's going to be extra context around an experiment that's
useful to use in publishing or when verifying results. There are a couple ways
to set this.

.. code:: python

    # The first is experiment-wide context, which will be set on every Observation an experiment makes
    experiment = laboratory.Experiment(name='Authorisation experiment', context={'action': action})

    # Context can also be set on an Observation-specific basis
    experiment.control(control_func, context={'strategy': 1})
    experiment.candidate(cand_func, context={'strategy': 2})

Context can be retrieved using the ``get_context`` method on ``Experiment`` and ``Observation`` instances.

.. code:: python

    class Experiment(laboratory.Experiment):
        def publish(self, result):
            self.get_context()
            result.control.get_context()
            result.candidates[0].get_context()


Ramping up
----------

Before running a candidate code block Laboratory will call ``Experiment.enabled``.
By overriding this method we can control when the candidate code will be executed.

For example, if we wanted to enable the experiment for just 10% of calls, we could
do something along these lines:

.. code:: python

    class MyExperiment(laboratory.Experiment):
        def enabled(self):
            return random.random() < 0.1

This is useful for slowly ramping up the experiment, but because we have access to
the experiment context in the ``enabled`` method, we're also able to do fancier
things like enabling only for specific users.

.. code:: python

    class MyExperiment(laboratory.Experiment):
        def enabled(self):
            ctx = self.get_context()
            return ctx['user'] in user_segment


Controlling comparison
----------------------

Not all data is created equal. By default laboratory compares using ``==``, but
sometimes you may need to tweak this to suit your needs.  It's easy enough |--|
subclass ``Experiment`` and implement the ``compare(control, candidate)`` method.

.. code:: python

    class MyExperiment(Experiment):
        def compare(self, control, candidate):
            return control.value['id'] == candidate.value['id']


Raise on mismatch
*****************

The ``Experiment`` class accepts a ``raise_on_mismatch`` argument which you can set
to ``True`` if you want Laboratory to raise an exception when the comparison returns
false. This may be useful in testing, for example.


Publishing results
------------------

This data is useless unless we can do something with it. Laboratory makes no
assumptions about how to do this |--| it's entirely for you to implement to suit
your needs.  For example, timing data can be sent to graphite, and mismatches
can be placed in a capped collection in redis for debugging later.

The publish method is passed a ``Result`` instance, with control and candidate
data is available in ``Result.control`` and ``Result.candidates``
respectively.

.. code:: python

    class MyExperiment(laboratory.Experiment):
        def publish(self, result):
            statsd.timing('MyExperiment.control', result.control.duration)
            for o in result.candidates:
                statsd.timing('MyExperiment.%s' % o.name, o.duration)


Caveats
-------

Because of the way Laboratory works, there are some situations in which it should
not be used. Namely, any code with side effects, such as disk or database writes,
or other state changes, are unsuitable as they'll lead to duplicated writes.
You could end up with buggy data or a candidate that affects the execution of
the control.

You’ll also take a performance hit by running your new code in addition to the old,
so be mindful of that. You should ramp an experiment up slowly and keep an eye on
your metrics.


Links
-----

- `Documentation <https://laboratory-python.readthedocs.io/en/latest/>`_
- `Source code <https://github.com/joealcorn/laboratory/>`_
- `CI server <https://travis-ci.org/joealcorn/laboratory/>`_
- `Python Package Index <https://pypi.python.org/pypi/laboratory>`_
- `Sure-footed refactoring <https://joealcorn.co.uk/blog/2018/sure-footed-refactoring>`_


Maintenance
-----------

Laboratory is actively maintained by Joe Alcorn (`Github <https://github.com/joealcorn>`_, `Twitter <https://twitter.com/joe_alcorn>`_)


.. |--| unicode:: U+2014  .. em dash
