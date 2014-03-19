from __future__ import absolute_import

import markdown

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed

from dmcm.models import Page

BLOG_ROOT = Page.objects.get(slug=settings.BLOG_ROOT_SLUG)


class LatestBlogPostsFeed(Feed):
    """
    RSS feed containing the latest blog entries.
    """
    site = Site.objects.get_current()
    title = '%s blog' % (site.domain)
    link = '/blog/'
    description = 'Recent Blog Entries.'

    def items(self):
        return Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if len(item.content) > 100:
            para_end = item.content.find('\n', 100)
            if para_end > 0:
                description = item.content[:para_end] + '...'
                return markdown.markdown(description, ['tables', 'toc'])
        return item.content

    def item_pubdate(self, item):
        return item.updated

    def item_link(self, item):
        return u'/%s/' % (item.slug)
