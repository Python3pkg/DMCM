"""
This command polls all of the Feeds and inserts or updates any new entries found.
"""
from django.core.management.base import BaseCommand
from feedreader.models import Feed
from feedreader.utils import poll_feed

import logging
logger = logging.getLogger('feedreader')

class Command(BaseCommand):
    args = 'none'
    help = 'Polls all Feeds for Entries.'

    def handle(self, *args, **options):
        """
        Read through all the feeds looking for new entries.
        """
        logger.info('Feedreader poll_feeds started')
        feeds = Feed.objects.all()
        for feed in feeds:
            poll_feed(feed)
        logger.info('Feedreader poll_feeds ended')
