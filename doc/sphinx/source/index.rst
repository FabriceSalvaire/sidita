.. include:: abbreviation.txt
.. include:: project-links.txt

.. raw:: html

    <style>
        .small-text {font-size: smaller}

	.spacer {height: 30px}

        .reduced-width {
	    max-width: 800px
        }

        .row {clear: both}

        @media only screen and (min-width: 1000px),
               only screen and (min-width: 500px) and (max-width: 768px){

            .column {
                padding-left: 5px;
                padding-right: 5px;
                float: left;
            }

            .column2  {
                width: 50%;
            }

            .column3  {
                width: 33.3%;
            }
        }
    </style>

.. raw:: html

   <div class="reduced-width">

########
 Title
########

.. image:: /_static/logo.png
   :alt: sidita logo
   :width: 750

********
Overview
********

Sidita is a Python module which implements a distributed task queue featuring an intermediate
solution between the |multiprocessing module|_ and a task scheduler like |Celery|_.

.. rst-class:: small-text

    (*) sidita is licensed under GPLv3 therms.

sidita requires Python 3 and works on Linux, Windows and OS X.

:ref:`To read more on sidita <overview-page>`

.. raw:: html

   <div class="spacer"></div>

.. rst-class:: clearfix row

.. rst-class:: column column2

:ref:`news-page`
================

What's changed in versions

.. rst-class:: column column2

:ref:`Installation-page`
========================

How to install sidita on your system

.. rst-class:: column column2

:ref:`user-faq-page`
====================

Answers to frequent questions

.. rst-class:: column column2

:ref:`first-steps-page`
=======================

First steps with sidita.

.. rst-class:: column column2

:ref:`development-page`
=======================

How to contribute to the project

.. rst-class:: column column2

:ref:`reference-manual-page`
============================

Technical reference material, for classes, methods, APIs, commands.

.. rst-class:: column column2

:ref:`how-to-refer-page`
========================

Guidelines to cite sidita

.. rst-class:: column column2

:ref:`donate-page`
==================

If you want to donate to the project or need a more professional support.

.. raw:: html

   </div>

.. why here ???

.. rst-class:: clearfix row

.. raw:: html

   <div class="spacer"></div>

*******************
 Table of Contents
*******************

.. toctree::
  :maxdepth: 3
  :numbered:

  overview.rst
  news.rst
  roadmap.rst
  installation.rst
  faq.rst
  design-notes.rst
  first-steps.rst
  reference-manual.rst
  development.rst
  how-to-refer.rst
  donate.rst
  related-projects.rst
  bibliography.rst
