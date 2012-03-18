from django.shortcuts import render_to_response, get_object_or_404
from dmcm.settings import DEBUG

from dmcm.cm.models import Page

def page(request, page_id):
    """Show Blog Entries, Pages and Lists which make up site."""
    page = get_object_or_404(Page, pk=page_id)
    context = {'page': page, 'debug': DEBUG}
    return render_to_response('page.html', context)
