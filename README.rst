Laboratory! |Build Status|
==========================

A Python library for carefully refactoring critical paths by testing in
production (inspired by `GitHub's Scientist`_) with support for Python 2.7, 3.3+

.. _GitHub's Scientist: https://github.com/github/scientist


- `Why?`_
- `Getting started`_
- `Adding context`_
- `Controlling comparison`_
    - `Raise on mismatch`_
- `Publishing results`_
- `Installation`_

.. _Why?:

Why?
----

Some blocks of code are more critical than the rest. Laboratory helps us refactor
important code paths with confidence by testing in production and verifying
the results.

By running experiments, Laboratory helps you establish a feedback loop which
you can use to make improvements to unproven code until the error rate is nil.

All non-trivial software has bugs, and bugs in code lead to bugs in data. This
means only production is production, and so testing in production is the only
way to ensure your code actually works.

I recommend reading Jesse Toth's `blog post`_ on using a similar techniques
within Github that inspired this library, as well as Charity Majors on
`why you should test in production`_.

.. _blog post: https://githubengineering.com/scientist/
.. _why you should test in production: https://opensource.com/article/17/8/testing-production


.. _Getting started:

Getting started
---------------

See: `Installation`_

With Laboratory you conduct an experiment with your known-good code as the
control block and a new code branch as a candidate. Laboratory will:

-  Run both the new and the old code
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

    experiment = laboratory.Experiment()
    with experiment.control() as c:
        c.record(authorise_control(action))

    with experiment.candidate() as c:
        c.record(authorise_candidate(action))

    authorised = experiment.conduct()


Note that the ``Experiment`` class can also be used as a decorator if the
control and candidate functions take the same arguments.

.. code:: python

    def authorise_candidate(action):
        return True

    @Experiment(candidate=authorise_candidate)
    def authorise_control(action):
        return True


An experiment will always return the value of the control block.


Adding context
--------------

A lot of the time there's going to be extra context around an experiment that's
useful to use in publishing or comparisons.  You can set this data in a few
ways.

.. code:: python

    # The first is experiment-wide context, which will be set on every observation laboratory makes
    experiment = laboratory.Experiment(name='Authorisation experiment', context={'action': action})

    # Observation-specific context can be updated before or as the experiment is running
    with experiment.control(context={'strategy': 1}) as c:
        e.update_context({'uuid': uuid})
        e.get_context()
        # {
        #     'action': 'delete',
        #     'strategy': 1,
        #     'uuid': 'c08d46f1-92a6-46e5-9185-82d90dcb5af1',
        # }

Context can be retrieved using the ``get_context`` method on ``Experiment`` and ``Observation`` classes.

.. code:: python

    class Experiment(laboratory.Experiment):
        def publish(self, result):
            self.get_context()
            result.control.get_context()
            result.observations[0].get_context()


Controlling comparison
----------------------

Not all data is created equal. By default laboratory compares using ``==``, but
sometimes you may need to tweak this to suit your needs.  It's easy enough |--|
just subclass ``Experiment`` and implement the ``compare(control,
observation)`` method.

.. code:: python

    class MyExperiment(Experiment):
        def compare(self, control, observation):
            return control.value['id'] == observation.value['id']


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
data is available in ``Result.control`` and ``Result.observations``
respectively.

.. code:: python

    class MyExperiment(laboratory.Experiment):
        def publish(self, result):
            statsd.timing('MyExperiment.control', result.control.duration)
            for o in result.observations:
                statsd.timing('MyExperiment.%s' % o.name, o.duration)


Installation
------------

Installing from pypi is recommended

.. code::

    $ pip install laboratory

You can also install a `tagged version`_ from Github

.. code::

    $ pip install https://github.com/joealcorn/laboratory/archive/v0.4.2.tar.gz

Or the latest development version

.. code::

    $ pip install git+https://github.com/joealcorn/laboratory.git


.. _tagged version: https://github.com/joealcorn/laboratory/releases


Maintenance
-----------

Laboratory is actively maintained by Joe Alcorn (`Github <https://github.com/joealcorn>`_, `Twitter <https://twitter.com/joe_alcorn>`_)


.. |--| unicode:: U+2014  .. em dash

.. |Build Status| image:: https://travis-ci.org/joealcorn/laboratory.svg?branch=master
   :target: https://travis-ci.org/joealcorn/laboratory
