from django.db import models


class Options(models.Model):
    """
    Options controlling fed reader behavior

    :Fields:

        number_initially_displayed : integer
            Number of entries, from all feeds, initially displayed on webpage.
        number_additionally_displayed : integer
            Number of entries added to webpage when scrolling down.
        max_entries_saved : integer
            Maximum number of entries to store for each feed.
    """
    number_initially_displayed = models.IntegerField(default=10)
    number_additionally_displayed = models.IntegerField(default=10)
    max_entries_saved = models.IntegerField(default=100)

    class Meta:
        verbose_name_plural = "options"

    def __unicode__(self):
        return u'Options'


class Group(models.Model):
    """
    Group of feeds.

    :Fields:

        name : char
            Name of group.
    """
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Feed(models.Model):
    """
    Feed information.

    :Fields:

        title : char
            Title of feed.
        xml_url : char
            URL of xml feed.
        link : char
            URL of feed site.
        description : text
            Description of feed.
        updated_time : date_time
            When feed was last updated.
        last_polled_time : date_time
            When feed was last polled.
        group : ForeignKey
            Group this feed is a part of.
    """
    title = models.CharField(max_length=250, blank=True, null=True)
    xml_url = models.CharField(max_length=250, unique=True)
    link = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    published_time = models.DateTimeField(blank=True, null=True)
    last_polled_time = models.DateTimeField(blank=True, null=True)
    group = models.ForeignKey(Group, blank=True, null=True)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title


class Entry(models.Model):
    """
    Feed entry information.

    :Fields:

        feed : ForeignKey
            Feed this entry is a part of.
        title : char
            Title of entry.
        link : char
            URL of entry.
        description : text
            Description of entry.
        updated_time : date_time
            When entry was last updated.
    """
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=250, blank=True, null=True)
    link = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)
    published_time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_time']
        verbose_name_plural = "entries"

    def __unicode__(self):
        return self.title


