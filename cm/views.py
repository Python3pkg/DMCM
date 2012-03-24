from django.shortcuts import render_to_response, get_object_or_404
from dmcm.settings import DEBUG
import datetime

from dmcm.cm.models import Page

def page(request, page_id):
    """Show Blog Entries, Pages and Lists which make up site."""
    page = get_object_or_404(Page, pk=page_id)
    context = {'page': page, 'debug': DEBUG}
    return render_to_response('page.html', context)

def site_map(request):
    """Build Site Map to display."""
    pages = Page.objects.all()
    root = Page.objects.get(pk=3)
    map_context = {'title': 'Index',
                   'parent': root,
                   'navigation_path': [{'title': root.title, 'address': '/'}],
                   'wide': False, 
                   'updated': datetime.datetime.now()
    }
    content = '# Site Map\n\nTitle | Parent | Updated\n-----|-----|-----\n'
    for page in pages:
        content += '['+page.title+'](/page/'+str(page.id)+') | '
        content += page.parent.title+' | '+page.updated.strftime("%Y-%m-%d %H:%M")+'\n'
    map_context['content'] = content
    context = {'page': map_context, 'debug': DEBUG}
    return render_to_response('page.html', context)