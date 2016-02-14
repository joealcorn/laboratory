# Laboratory! [![Build Status](https://travis-ci.org/joealcorn/laboratory.svg?branch=master)](https://travis-ci.org/joealcorn/laboratory)

A Python library for carefully refactoring critical paths (and a port of [Github's Scientist](https://github.com/github/scientist)).


## Why?

See Github's blog post - http://githubengineering.com/scientist/


## But how?

Imagine you've implemented a complex caching strategy for some objects in your database and a stale cache is simply not acceptable.
How could you test this and ensure parity with your previous implementation, under load, with production data?
Run it in production!

```python
import laboratory

experiment = laboratory.Experiment()
with experiment.control() as c:
    c.record(get_objects_from_database())

with experiment.candidate() as c:
    c.record(get_objects_from_cache())

objects = experiment.run()
```

Mark the original code as the control and any other implementations as candidates. Timing information is recorded about all control
and candidate blocks, and any exceptions from the candidates will be swallowed so they don't affect availability.
Laboratory will always return the result of the control block.


## Publishing results

This data is useless unless we can do something with it. Laboratory makes no assumptions about how to do this - it's entirely for you
to implement to suit your needs.
For example, timing data can be sent to graphite, and mismatches can be placed in a capped collection in redis for debugging later.

The publish method is passed a `Result` instance, with control and candidate data is available in `Result.control` and `Result.observations`
respectively.


## Controlling comparison

Not all data is created equal. By default laboratory compares using `==`, but sometimes you may need to tweak this to suit your needs.
It's easy enough - just subclass `Experiment` and implement the `compare(control, observation)` method.

```python

class MyExperiment(Experiment):
    def compare(self, control, observation):
        return control.value['id'] == observation.value['id']
```
