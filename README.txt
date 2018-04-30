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

.. include:: features.txt

.. include:: technical_brief.txt

How to install it ?
-------------------

Look at the `installation <https://fabricesalvaire.github.io/sidita/installation.html>`_ section in the documentation.

Credits
=======

Authors: `Fabrice Salvaire <http://fabrice-salvaire.fr>`_

News
====

.. include:: news.txt
