import feedparser
from datetime import datetime
from time import mktime
from feedreader.models import Feed, Entry, Options

import logging
logger = logging.getLogger('feedreader')

def poll_feed(feed, verbose=False):
    """
    Read through a feed looking for new entries.
    """
    options = Options.objects.all()[0]
    f = feedparser.parse(feed.xml_url)
    if hasattr(f.feed, 'bozo_exception'):
        # Malformed feed
        logger.warning('Feedreader poll_feeds found Malformed feed, %s: %s' % (feed.xml_url, f.feed.bozo_exception))
        return
    if hasattr(f.feed, 'published_parsed'):
        published_time = datetime.fromtimestamp(mktime(f.feed.published_parsed))
        if feed.published_time and feed.published_time >= published_time:
            return
        feed.published_time = published_time
    for attr in ['title', 'link', 'description']:
        if not hasattr(f.feed, attr):
            logger.error('Feedreader poll_feeds. Feed "%s" has no %s' % (feed.xml_url, attr))
            return
    feed.title = f.feed.title
    feed.link = f.feed.link
    feed.description = f.feed.description
    feed.last_polled_time = datetime.now()
    feed.save()
    if verbose:
        print('%d entries to process in %s' % (len(f.entries), feed.title))
    for i, e in enumerate(f.entries):
        if i > options.max_entries_saved:
            break
        for attr in ['title', 'link', 'description']:
            if not hasattr(e, attr):
                logger.error('Feedreader poll_feeds. Entry "%s" has no %s' % (e.link, attr))
                continue
        entry, created = Entry.objects.get_or_create(feed=feed, link=e.link)
        if created:
            if hasattr(e, 'published_parsed'):
                published_time = datetime.fromtimestamp(mktime(e.published_parsed))
                entry.published_time = published_time
            entry.feed = feed
            entry.title = e.title
            entry.description = e.description
            entry.save()
