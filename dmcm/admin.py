from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput, Textarea
from project.dmcm.models import Page
from reversion.admin import VersionAdmin


class PageAdmin(VersionAdmin):
    search_fields = ['title']
    list_display = ['title', 'parent', 'updated', 'wide']
    list_filter = ['wide']
    list_editable = ['wide']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['updated']
    ordering = ['parent', 'title']
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': (('content',),
                       ('title', 'parent',),
                       ('slug',),
                       ('published', 'updated'),
                       ('wide',),
                       )
        }),
    )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 60})},
        models.TextField: {'widget': Textarea(attrs={'rows': 25, 'cols': 110})},
    }

admin.site.register(Page, PageAdmin)

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    readonly_fields = LogEntry._meta.get_all_field_names() + ['object_link', 'action_description']

    list_filter = ['user', 'content_type', 'action_flag']

    search_fields = ['object_repr', 'change_message']

    list_display = ['action_time', 'user', 'content_type', 'object_link',
                    'action_description', 'change_message']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model),
                        args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def action_description(self, obj):
        action_names = {
            ADDITION: 'Addition',
            DELETION: 'Deletion',
            CHANGE: 'Change',
        }
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'

admin.site.register(LogEntry, LogEntryAdmin)
