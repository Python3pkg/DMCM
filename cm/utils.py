from dmcm.settings import DEBUG, SITE_ROOT_ID

def context_processor(request):
    return {'DEBUG': DEBUG, 'SITE_ROOT_ID': SITE_ROOT_ID}

from django.contrib.syndication.views import Feed
from dmcm.cm.models import Page
from dmcm.settings import BLOG_ROOT_ID
import markdown

BLOG_ROOT = Page.objects.get(pk=BLOG_ROOT_ID)

class LatestBlogPostsFeed(Feed):
    title = "ahernp.com blog"
    link = "/blog/"
    description = "Recent Blog Entries."

    def items(self):
        return Page.objects.filter(parent__exact=BLOG_ROOT).order_by('-published')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if len(item.content) > 100:
            para_end = item.content.find('\n', 100)
            if para_end > 0: 
                description = item.content[:para_end]+'...'
                return markdown.markdown(description, ['tables', 'toc',])
        return item.content

    def item_link(self, item):
        return u'/page/%d/' % (item.id)