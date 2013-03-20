from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from feedreader.models import Options, Group, Feed, Entry
from feedreader.utils import poll_feed


def get_context(get):
    """Build common context dictionary""" 
    poll_flag = get.get('poll_flag', None)
    feed = None
    feed_id = get.get('feed_id', None)
    if feed_id:
        try:
            feed = Feed.objects.get(pk=feed_id)
        except Feed.DoesNotExist:
            pass
    group = None
    group_id = get.get('group_id', None)
    if group_id:
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            pass
    context = {}
    options = Options.objects.all()[0]
    if feed:
        if poll_flag:
            poll_feed(feed)
        entries = Entry.objects.filter(feed=feed)[:options.number_initially_displayed]
        context['entries_header'] = feed.title
    elif group:
        feeds = Feed.objects.filter(group=group)
        if poll_flag:
            for feed in feeds:
                poll_feed(feed)
        entries = Entry.objects.filter(feed__group=group)[:options.number_initially_displayed]
        context['entries_header'] = group.name
    else:
        entries = Entry.objects.all()[:options.number_initially_displayed]
        context['entries_header'] = 'All items'
    context['entries'] = entries
    return context


@login_required
def ajax_get_feeds(request):
    """Get feed contents"""
    context = get_context(request.GET)
    return render_to_response('feedreader/feed_entries.html', context, RequestContext(request))


@login_required
def feeds(request):
    """Show most recent feed contents on page"""
    context = get_context(request.GET)
    context['groups'] = Group.objects.all()
    context['no_group'] = Feed.objects.filter(group=None)
    context['feed_meta'] = Feed._meta
    return render_to_response('feedreader/feeds.html', context, RequestContext(request))
