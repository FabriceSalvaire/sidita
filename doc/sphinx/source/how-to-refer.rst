.. _how-to-refer-page:

===========================
 How to Refer to sidita ?
===========================

Up to now, the official url for sidita is @project_url@

*A permanent redirection will be implemented if the domain change in the future.*

On Github, you can use the **sidita** `topic <https://github.com/search?q=topic%3Asidita&type=Repositories>`_ for repository related to sidita.

A typical `BibTeX <https://en.wikipedia.org/wiki/BibTeX>`_ citation would be, for example:

.. code:: bibtex

    @software{sidita,
      author = {Fabrice Salvaire}, % actual author and maintainer
      title = {sidita},
      url = {@project_url@},
      version = {x.y},
      date = {yyyy-mm-dd}, % set to the release date
    }

    @Misc{sidita,
      author = {Fabrice Salvaire},
      title = {sidita},
      howpublished = {\url{@project_url@}},
      year = {yyyy}
    }
