import feedparser
from datetime import datetime
from time import mktime
from feedreader.models import Feed, Entry

import logging
logger = logging.getLogger('feedreader')

def poll_feed(feed):
    """
    Read through a feed looking for new entries.
    """
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
    feed.title = f.feed.title
    feed.link = f.feed.link
    feed.description = f.feed.description
    feed.last_polled_time = datetime.now()
    feed.save()
    for e in f.entries:
        entry, created = Entry.objects.get_or_create(feed=feed, link=e.link)
        if hasattr(e, 'published_parsed'):
            published_time = datetime.fromtimestamp(mktime(e.published_parsed))
            if (not created and 
                entry.published_time and 
                entry.published_time >= published_time):
                continue
            entry.published_time = published_time
        elif not created and entry.title == e.title and entry.description == e.description:
            continue
        entry.feed = feed
        entry.title = e.title
        entry.description = e.description
        entry.save()
