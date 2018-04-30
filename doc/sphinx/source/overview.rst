.. include:: abbreviation.txt
.. include:: project-links.txt

.. _overview-page:

==========
 Overview
==========

What is Sidita ?
----------------

Sidita is a Python module which implements a distributed task queue featuring an intermediate
solution between the |multiprocessing module|_ and a task scheduler like |Celery|_.

The Sidita use case corresponds to the case where you need to run CPU bound tasks in parallel and
you require an immunity to crashes, memory leaks and overruns.  Theses requirements are met by a
monitored subprocess implementation.

How is Sidita licensed ?
------------------------

Sidita is licensed under the `GPLv3 <https://www.gnu.org/licenses/quick-guide-gplv3.en.html>`_.

Going further with Sidita
-------------------------

The best way to know what you can do with Sidita, and to learn it, is to look these pages :

 * :ref:`First Steps <first-steps-page>`
 * :ref:`Sidita Reference Manual <reference-manual-page>`

Which platforms are supported by Sidita ?
-----------------------------------------

Sidita runs on Linux, Windows 64-bit and Mac OS X.

How to install Sidita ?
-----------------------

The procedure to install Sidita is described in the :ref:`Installation Manual <installation-page>`.

Which version of Python is required ?
-------------------------------------

Sidita requires Python 3 and the version 3.5 is recommended so as to benefit from the new *@* syntax
for units.
