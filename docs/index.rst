.. Laboratory documentation master file, created by
   sphinx-quickstart on Fri Jan 19 23:43:02 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Laboratory
==========

A Python library for carefully refactoring critical paths with support for Python 2.7 & 3.3+

Laboratory helps us refactor important code paths with confidence. By conducting experiments
and verifying their results, we can not only see if our unproven code is misbehaving, we have
established a feedback loop that we can use to guide us towards the correct behaviour.


.. note:: These docs are a work in progress. More complete documentation can be found on the
          `project's github page <https://github.com/joealcorn/laboratory>`_


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   reference

.. _quickstart:

Quickstart
----------

See: :ref:`installation`

With Laboratory you conduct an experiment with your known-good code as the
control block and a new code branch as a candidate.


Let's do an experiment together::

    import laboratory

    # create an experiment
    experiment = laboratory.Experiment()

    # set your control and candidate functions
    experiment.control(authorise_control, args=(user,))
    experiment.candidate(authorise_candidate, args=(user,))

    # conduct the experiment and return the control value
    authorised = experiment.conduct()

Laboratory just:

-  Ran the unproven (candidates) and the existing (control) code
-  Compared the return values
-  Recorded timing information about all code
-  Caught (and logged) exceptions in the unproven code
-  Published all of this information

.. Note::

    By default publish is a no-op. See `Publishing results <https://github.com/joealcorn/laboratory#publishing-results>`_


That's it as far as laboratory goes; the time consuming part will be implementing your
candidates correctly.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`


.. |badge_pypi| image:: https://badge.fury.io/py/laboratory.svg
   :target: https://pypi.python.org/pypi/laboratory
