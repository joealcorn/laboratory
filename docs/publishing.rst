.. _publishing:

Publishing results
==================

We saw in the :ref:`quickstart` how to create and run an experiment. Now let's see
how we can take the data gathered in that experiment and publish it to make it
useful to us.

Laboratory makes no assumptions about how to do this |--| it's entirely for you to
implement to suit your needs. For example, timing data can be sent to graphite,
and mismatches could be written to disk for debugging at a later date.

Publishing
----------

To publish, you must implement the :func:`publish` method on an :class:`Experiment`.

The publish method is passed a :ref:`ref_result` instance, with control and candidate
observations available under ``result.control`` and ``result.candidates`` respectively.


.. automethod:: laboratory.experiment.Experiment.publish
    :noindex:


StatsD implementation
---------------------

Here's an example implementation for statsd::

    class StatsdExperiment(laboratory.Experiment):
        def publish(self, result):
            if result.match:
                statsd.incr('experiment.match')
            else:
                statsd.incr('experiment.mismatch')

            statsd.timing('experiment.control', result.control.duration)
            for obs in result.candidates:
                statsd.timing('experiment.%s' % obs.name, obs.duration)


.. |--| unicode:: U+2014  .. em dash
