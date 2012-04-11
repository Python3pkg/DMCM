# DMCM

Django Markdown Content Manager is the application used to implement my personal website [ahernp.com](http:/ahernp.com).

The site has a very simple structure. Features:

* A single model: Page. The content of each page is held in Markdown format. Almost everything on the site is a page.
* Class-based generic views are used to show individual pages and lists of pages.
* Site-wide string-search.
* Context processor to make some variables available to all templates.
* Command to `check_mysql_structure` matches what the Models expect.

Dependencies:

* Uses [django-reversion](https://github.com/etianen/django-reversion) to keep a history of changes.
