Laboratory! |Build Status|
==========================

A Python library for carefully refactoring critical paths (and a port of
`GitHub's Scientist`_).

.. _GitHub's Scientist: https://github.com/github/scientist


- `Installation`_
- `Getting started`_
- `Publishing results`_
- `Controlling comparison`_
- `Adding context`_


Why?
----

See GitHub's blog post |--| http://githubengineering.com/scientist/


.. _Getting started:

But how?
--------

Imagine you've implemented a complex caching strategy for some objects in your
database and a stale cache is simply not acceptable.  How could you test this
and ensure parity with your previous implementation, under load, with
production data?  Run it in production!

Laboratory will:

-  Run both the new and the old code
-  Compare their results
-  Record timing information about all code
-  Swallow and record exceptions in the new code
-  Publish all of this information

Of course, you're still unsure your candidate code works correctly, so
laboratory will always return the result from the control block.

.. code:: python

    import laboratory

    experiment = laboratory.Experiment()
    with experiment.control() as c:
        c.record(get_objects_from_database())

    with experiment.candidate() as c:
        c.record(get_objects_from_cache())

    objects = experiment.conduct()

Note that the ``Experiment`` class can also be used as a decorator.

.. code:: python

    @Experiment(candidate=get_objects_from_cache)
    def get_objects_from_database():
        return True


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


Adding context
--------------

A lot of the time there's going to be extra context around an experiment that's
useful to use in publishing or comparisons.  You can set this data in a few
ways.

.. code:: python

    # The first is experiment-wide context, which will be set on every observation laboratory makes.

    experiment = laboratory.Experiment(name='Object Cache Experiment', context={'user': user})


    # Observation-specific context can be updated before or as the experiment is running.

    with experiment.control(name='Object DB Strategy', context={'using': 'db'}) as e:
        e.update_context({'uuid': uuid})

        e.get_context()
        # {
        #     'user': <User>,
        #     'uuid': 'c08d46f1-92a6-46e5-9185-82d90dcb5af1',
        #     'using': 'db',
        # }


    with experiment.candidate(name='Object Cache Strategy', context={'using': 'cache'}) as e:
        e.update_context({'uuid': uuid})

        e.get_context()
        # {
        #     'user': <User>,
        #     'using': 'cache',
        # }


Context can be retrieved using the ``get_context`` method on ``Experiment`` and ``Observation`` classes.

.. code:: python

    class Experiment(laboratory.Experiment):

        def publish(self, result):
            self.get_context()
            result.control.get_context()
            result.observations[0].get_context()


Installation
------------

Installing from pypi is recommended

.. code::

    $ pip install laboratory


Maintenance
-----------

Laboratory is actively maintained by Joe Alcorn (`Github <https://github.com/joealcorn>`_, `Twitter <https://twitter.com/joe_alcorn>`_)


.. |--| unicode:: U+2014  .. em dash

.. |Build Status| image:: https://travis-ci.org/joealcorn/laboratory.svg?branch=master
   :target: https://travis-ci.org/joealcorn/laboratory
