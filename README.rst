Django Markdown Content Manager
===============================

DMCM is a Django 1.6 app which implements a content management
system where every item is a page and all the content is written
in Markdown.


Quick start
-----------

1. Add "dmcm" to your INSTALLED\_APPS setting like this::

     INSTALLED\_APPS = ( ... 'feedreader', )

2. Include the feedreader URLconf in your project urls.py like this::

     url(r'^dmcm/', include('dmcm.urls')),

3. Run ``python manage.py syncdb`` to create the dmcm models.

4. Run ``python manage.py collectstatic`` to copy static files to your
   project's static root.


Dependencies
------------

-  `Django 1.6.2 <https://pypi.python.org/pypi/Django/1.6.2>`__
-  `feedparser <https://pypi.python.org/pypi/feedparser>`__
-  `pytz <https://pypi.python.org/pypi/pytz/2013.9>`__

