from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from feedreader.models import Options, Group, Feed, Entry
from feedreader.utils import poll_feed


@transaction.commit_manually
def flush_transaction():
    """Flush the current transaction so as not to read stale data."""
    transaction.commit()


def build_context(get):
    """Build common context dictionary""" 
    context = {}
    poll_flag = get.get('poll_flag', None)
    mark_read_flag = get.get('mark_read_flag', None)
    show_read_flag = get.get('show_read_flag', None)
    context['show_read_flag'] = show_read_flag
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
    options = Options.objects.all()[0]
    if feed:
        if mark_read_flag:
            entries = Entry.objects.filter(feed=feed, read=False)
            entries.update(read=True)
        if poll_flag:
            poll_feed(feed)
        if show_read_flag:
            entries = Entry.objects.filter(feed=feed)  # [:options.number_initially_displayed]
        else:
            entries = Entry.objects.filter(feed=feed, read=False)  # [:options.number_initially_displayed]
        context['entries_header'] = feed.title
    elif group:
        feeds = Feed.objects.filter(group=group)
        if mark_read_flag:
            entries = Entry.objects.filter(feed__group=group, read=False)
            entries.update(read=True)
        if poll_flag:
            for feed in feeds:
                poll_feed(feed)
        if show_read_flag:
            entries = Entry.objects.filter(feed__group=group)[:options.number_initially_displayed]
        else:
            entries = Entry.objects.filter(feed__group=group, read=False)[:options.number_initially_displayed]
        context['entries_header'] = group.name
    else:
        if mark_read_flag:
            entries = Entry.objects.filter(read=False)
            entries.update(read=True)
        if show_read_flag:
            entries = Entry.objects.all()[:options.number_initially_displayed]
        else:
            entries = Entry.objects.filter(read=False)[:options.number_initially_displayed]
        context['entries_header'] = 'All items'
    context['entries'] = entries
    return context


@login_required
def ajax_get_num_unread(request):
    """Count numbers of unread entries"""
    flush_transaction()  # Ensure latest data is read from database
    context = {}
    context['unread_total'] = Entry.objects.filter(read=False).count()
    groups = Group.objects.all()
    for group in groups:
        num_unread = Entry.objects.filter(feed__group=group, read=False).count()
        context['unread_group%s' % (group.id)] = num_unread
        context['unread_group_button%s' % (group.id)] = num_unread
    feeds = Feed.objects.all()
    for feed in feeds:
        context['unread_feed%s' % (feed.id)] = Entry.objects.filter(feed=feed, read=False).count()
    return HttpResponse(simplejson.dumps(context), mimetype='application/json')


@login_required
def ajax_get_feeds(request):
    """Get feed contents"""
    context = build_context(request.GET)
    return render_to_response('feedreader/feed_entries.html', context, RequestContext(request))


@login_required
def feeds(request):
    """Show most recent feed contents on page"""
    context = build_context(request.GET)
    context['groups'] = Group.objects.all()
    context['no_group'] = Feed.objects.filter(group=None)
    context['feed_meta'] = Feed._meta
    return render_to_response('feedreader/feeds.html', context, RequestContext(request))
