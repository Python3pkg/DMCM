from django.contrib import admin
from feedreader.models import Options, Group, Feed, Entry
from reversion.admin import VersionAdmin


class OptionsAdmin(VersionAdmin):
    list_display = ['number_initially_displayed', 'number_additionally_displayed', 'max_entries_saved']

admin.site.register(Options, OptionsAdmin)


class GroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(Group, GroupAdmin)


class FeedAdmin(admin.ModelAdmin):
    list_display = ['xml_url', 'title', 'group', 'published_time', 'last_polled_time']
    list_filter = ['group']
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


class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'published_time']
    list_filter = ['feed']
    search_fields = ['title', 'link']
    readonly_fields = ['published_time', 'feed']
    fieldsets = (
        (None, {
            'fields': (('title',),
                       ('link',),
                       ('published_time',),
                       ('description',),
                       ('feed', 'read_flag'),
                       )
        }),
    )

admin.site.register(Entry, EntryAdmin)
