"""
This command polls all of the Feeds and inserts or updates any new entries found.
"""
from optparse import make_option
from django.core.management.base import BaseCommand
from feedreader.models import Feed, Entry, Options
from feedreader.utils import poll_feed

import logging
logger = logging.getLogger('feedreader')

class Command(BaseCommand):
    args = 'none'
    help = 'Polls all Feeds for Entries.'
    option_list = BaseCommand.option_list + (
    make_option('--verbose',
        action='store_true',
        dest='verbose',
        default=False,
        help='Print progress on command line'),
    )

    def handle(self, *args, **options):
        """
        Read through all the feeds looking for new entries.
        """
        logger.info('Feedreader poll_feeds started')
        verbose = options['verbose']
        options = Options.objects.all()[0]
        feeds = Feed.objects.all()
        if verbose:
            print('%d feeds to process' % (len(feeds)))
        for feed in feeds:
            if verbose:
                print('Processing Feed %s' % (feed.title))
            poll_feed(feed, verbose)
            # Remove older entries
            entries = Entry.objects.filter(feed=feed)[options.max_entries_saved:]
            for entry in entries:
                entry.delete()
            if verbose:
                print('Deleted %d entries from feed %s' % ((len(entries), feed.title)))
        logger.info('Feedreader poll_feeds ended')
