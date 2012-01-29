from django.contrib.syndication.views import Feed
from dmcm.cm.models import BlogPage, Option

class LatestEntriesFeed(Feed):
    title = "ahernp.com blog"
    link = "/blog/"
    description = "Recent entries on ahernp.com blog."

    def items(self):
        return BlogPage.objects.order_by('-date')[:10]

    def item_link(self, item):
        option = Option.objects.get(pk=1)
        return "/"+option.blog_deploy_dir+\
            item.date.isoformat()+"-"+item.filename+".html"

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return "Published on: "+item.date.isoformat()+"."
