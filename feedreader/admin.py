from django.contrib import admin
from feedreader.models import Options, Group, Feed, Entry
from reversion.admin import VersionAdmin


class OptionsAdmin(VersionAdmin):
    list_display = ['number_initially_displayed', 'number_additionally_displayed', 'max_entries_saved']

admin.site.register(Options, OptionsAdmin)


class GroupAdmin(VersionAdmin):
    pass

admin.site.register(Group, GroupAdmin)


class FeedAdmin(VersionAdmin):
    list_display = ['xml_url', 'title', 'group', 'published_time', 'last_polled_time']
    search_fields = ['link', 'title']
    readonly_fields = ['last_polled_time']
    fieldsets = (
        (None, {
            'fields': (('title',),
                       ('xml_url', 'link',),
                       ('published_time', 'last_polled_time',),
                       ('description',),
                       ('group',),
                       )
        }),
    )

admin.site.register(Feed, FeedAdmin)


class EntryAdmin(VersionAdmin):
    list_display = ['link', 'title', 'feed', 'published_time']
    search_fields = ['link', 'title']
    readonly_fields = ['published_time', 'feed']
    fieldsets = (
        (None, {
            'fields': (('title',),
                       ('link',),
                       ('published_time',),
                       ('description',),
                       ('feed', 'read'),
                       )
        }),
    )

admin.site.register(Entry, EntryAdmin)
