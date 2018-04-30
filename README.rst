.. -*- Mode: rst -*-

.. -*- Mode: rst -*-

..
   |siditaUrl|
   |siditaHomePage|_
   |siditaDoc|_
   |sidita@github|_
   |sidita@readthedocs|_
   |sidita@readthedocs-badge|
   |sidita@pypi|_

.. |ohloh| image:: https://www.openhub.net/accounts/230426/widgets/account_tiny.gif
   :target: https://www.openhub.net/accounts/fabricesalvaire
   :alt: Fabrice Salvaire's Ohloh profile
   :height: 15px
   :width:  80px

.. |siditaUrl| replace:: https://fabricesalvaire.github.io/sidita

.. |siditaHomePage| replace:: sidita Home Page
.. _siditaHomePage: https://fabricesalvaire.github.io/sidita

.. |sidita@readthedocs-badge| image:: https://readthedocs.org/projects/sidita/badge/?version=latest
   :target: http://sidita.readthedocs.org/en/latest

.. |sidita@github| replace:: https://github.com/FabriceSalvaire/sidita
.. .. _sidita@github: https://github.com/FabriceSalvaire/sidita

.. |sidita@pypi| replace:: https://pypi.python.org/pypi/sidita
.. .. _sidita@pypi: https://pypi.python.org/pypi/sidita

.. |Build Status| image:: https://travis-ci.org/FabriceSalvaire/sidita.svg?branch=master
   :target: https://travis-ci.org/FabriceSalvaire/sidita
   :alt: sidita build status @travis-ci.org

.. |Pypi Version| image:: https://img.shields.io/pypi/v/sidita.svg
   :target: https://pypi.python.org/pypi/sidita
   :alt: sidita last version

.. |Pypi License| image:: https://img.shields.io/pypi/l/sidita.svg
   :target: https://pypi.python.org/pypi/sidita
   :alt: sidita license

.. |Pypi Python Version| image:: https://img.shields.io/pypi/pyversions/sidita.svg
   :target: https://pypi.python.org/pypi/sidita
   :alt: sidita python version

..  coverage test
..  https://img.shields.io/pypi/status/Django.svg
..  https://img.shields.io/github/stars/badges/shields.svg?style=social&label=Star
.. -*- Mode: rst -*-

.. |Python| replace:: Python
.. _Python: http://python.org

.. |PyPI| replace:: PyPI
.. _PyPI: https://pypi.python.org/pypi

.. |Sphinx| replace:: Sphinx
.. _Sphinx: http://sphinx-doc.org

.. |asyncio| replace:: asyncio
.. _asyncio: https://docs.python.org/3/library/asyncio.html

.. |asyncio event loop| replace:: asyncio event loop
.. _asyncio event loop: https://docs.python.org/3/library/asyncio-eventloops.html

.. |asyncio queue| replace:: asyncio queue
.. _asyncio queue: https://docs.python.org/3/library/asyncio-queue.html

.. |asyncio subprocess| replace:: asyncio subprocess
.. _asyncio subprocess: https://docs.python.org/3/library/asyncio-subprocess.html

.. |multiprocessing module| replace:: multiprocessing module
.. _multiprocessing module: https://docs.python.org/3.6/library/multiprocessing.html

.. |Celery| replace:: Celery
.. _Celery: http://www.celeryproject.org

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

.. -*- Mode: rst -*-


.. no title here

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

.. -*- Mode: rst -*-


.. no title here

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

.. -*- Mode: rst -*-


.. no title here

V0 2018-05-01
-------------

Started project
