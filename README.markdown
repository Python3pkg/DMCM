====
DMCM
====

Django Markdown Content Manager is the application used on my personal 
website [ahernp.com](http:/ahernp.com).

Features
--------

* A single model: Page. The content of each page is held in Markdown 
  format. Almost everything on the site is a page.
* Class-based generic views are used to show individual pages and lists 
  of pages.
* Site-wide string-search.
* Context processor to make some variables available to all templates.

Dependencies
------------

* [Django 1.5](https://pypi.python.org/pypi/Django/1.5) web framework.
* [Markdown](https://pypi.python.org/pypi/Markdown) text-to-HTML 
  converter.
* Uses [django-reversion](https://github.com/etianen/django-reversion)
  to keep a history of changes.
* [django-feedreader](https://github.com/ahernp/django-feedreader) 
  RSS feed aggregator.
