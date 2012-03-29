# DMCM

Djang Markdown Content Manager is the application used to implement my personal website
[ahernp.com](http:/ahernp.com).

The site has a very simple structure:

* A single model: Page. The content of each page is held in Markdown format. Almost everything on the site is a page.
* Class-based generic views are used to build individual pages and lists of pages.
* Site-wide string-search.
* Uses [django-reversion](https://github.com/etianen/django-reversion) to keep a history of changes.

Features/example code to be added:

* Natural Keys.
* Fixtures.
* Command to check structure of MySQL against models.
