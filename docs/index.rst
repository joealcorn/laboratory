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

.. toctree::
   :maxdepth: 2

   Index & Quickstart <self>
   installation
   publishing
   reference


.. note:: These docs are a work in progress. Additional documentation can be found on the
          `project's github page <https://github.com/joealcorn/laboratory>`_


.. _quickstart:

Quickstart
----------

See: :ref:`installation` or ``pip install laboratory``


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

-  Executed the unproven (candidates) and the existing (control) code
-  Compared the return values
-  Recorded timing information about all code
-  Caught (and logged) exceptions in the unproven code
-  Published all of this information (see :ref:`publishing`)

For the most part that's all there is to it. You'll need to do some work to :ref:`publish your results <publishing>`
in order to act on the experiment, but if you've got a metrics solution ready to go it should be straightforward.

If you need to `control comparison`_, you can do that too.

.. Tip::

    Your control and candidate functions execute in a random order to help catch ordering issues


.. _control comparison: https://github.com/joealcorn/laboratory#controlling-comparison


Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
