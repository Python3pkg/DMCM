from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput, Textarea
from project.dmcm.models import Page
from reversion.admin import VersionAdmin

class PageAdmin(VersionAdmin):
    list_display = ('title', 'parent', 'updated', 'wide')
    list_filter = ('wide',)
    list_editable = ('wide',)
    readonly_fields = ('updated',)
    ordering = ('parent', 'title',)
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': (('content',),
                       ('title', 'parent',),
                       ('wide', 'published', 'updated'),
                       )
        }),
    )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':70})},
        models.TextField: {'widget': Textarea(attrs={'rows':25, 'cols':110})},
    }

admin.site.register(Page, PageAdmin)