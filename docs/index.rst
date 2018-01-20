.. Laboratory documentation master file, created by
   sphinx-quickstart on Fri Jan 19 23:43:02 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Laboratory
==========

A Python library for carefully refactoring critical paths with support for Python 2.7, 3.3+

Laboratory helps us refactor important code paths with confidence by conducting experiments
and verifying the results.


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
control block and a new code branch as a candidate. Laboratory will then:

-  Run both the new (candidate) and the old (control) code
-  Compare the return values
-  Record timing information about old & new code
-  Catch (but record!) exceptions in the new code
-  Publish all of this information

Let's see how to set up an experiment


.. code:: python

    import laboratory

    # set up the experiment and define control and candidate functions
    experiment = laboratory.Experiment()
    experiment.control(authorise_control, args=(user,))
    experiment.candidate(authorise_candidate, args=(user,))

    # conduct the experiment and return the control value
    authorised = experiment.conduct()


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |badge_pypi| image:: https://badge.fury.io/py/laboratory.svg
   :target: https://pypi.python.org/pypi/laboratory
