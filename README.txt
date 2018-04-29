.. -*- Mode: rst -*-

.. include:: project-links.txt
.. include:: abbreviation.txt

============
 sidita
============

|Pypi License|
|Pypi Python Version|

|Pypi Version|

* Quick Link to `Production Branch <https://github.com/FabriceSalvaire/sidita/tree/master>`_
* Quick Link to `Devel Branch <https://github.com/FabriceSalvaire/sidita/tree/devel>`_

Overview
========

What is sidita ?
---------------------

Sidita is a Python module which implements a distributed task queue featuring an intermediate
solution between the |multiprocessing module|_ and a task scheduler like |Celery|_.

The Sidita use case corresponds to the case where you need to run CPU bound tasks in parallel and
you require an immunity to crashes, memory leaks and overruns.  Theses requirements are met by a
monitored subprocess implementation.

Where is the Documentation ?
----------------------------

The documentation is available on the |siditaHomePage|_.

What are the main features ?
----------------------------

* Must be a simple solution to circumvent to the GIL limitation : i.e. distribute and run tasks in parallel on local CPU cores
* Must be a lightweight solution to Celery : no broker
* Should be portable on main OS like Unix and Windows
* Scheduler is implemented using an |asyncio event loop|_ and |asyncio queue|_
* Scheduler queue can be limited on size so as to prevent a memory overshoot at startup
* Workers are spawned using |asyncio subprocess|_ and communicate through a pipe (stdin, stdout)
* Pass any pickable object as request and response
* Scheduler monitors workers and restart them when they was killed or they exceeded a memory or timeout threshold
* Provide basic metrics on workers

Technical details in brief:

* scheduler run a producer and N consumers coroutines in an |asyncio|_ event loop
* the producer coroutine awaits on :code:`queue.put(task)` ( if a size limit is set )
* each consumer coroutine wraps a worker subprocess and await data on the stdout pipe

How to install it ?
-------------------

Look at the `installation <https://fabricesalvaire.github.io/sidita/installation.html>`_ section in the documentation.

Credits
=======

Authors: `Fabrice Salvaire <http://fabrice-salvaire.fr>`_

News
====

.. include:: news.txt
