from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from feed_reader.models import Options, Group, Feed, Entry

@login_required
def feeds(request):
    """Show most recent feed contents on page"""
    feed = None
    feed_id = request.GET.get('feed', None)
    if feed_id:
        try:
            feed = Feed.objects.get(pk=feed_id)
        except Feed.DoesNotExist:
            pass
    group = None
    group_id = request.GET.get('group', None)
    if group_id:
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            pass
    context = {}
    context['object'] = {'wide': True}  # Use wide webpage layout 
    options = Options.objects.get(pk=1)
    if feed:
        entries = Entry.objects.filter(feed=feed)[:options.number_initially_displayed]
        context['entries_header'] = feed.title
    elif group:
        entries = Entry.objects.filter(feed__group=group)[:options.number_initially_displayed]
        context['entries_header'] = group.name
    else:
        entries = Entry.objects.all()[:options.number_initially_displayed]
        context['entries_header'] = 'All items'
    context['entries'] = entries
    context['groups'] = Group.objects.all()
    context['no_group'] = Feed.objects.filter(group=None)
    # groups[0].feed_set.all()
    return render_to_response('feeds.html', context, RequestContext(request))
