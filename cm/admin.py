from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput, Textarea
from dmcm.cm.models import Page
from reversion.admin import VersionAdmin

class PageAdmin(VersionAdmin):
    list_display = ('title', 'parent', 'updated', 'wide')
    list_filter = ('wide',)
    list_editable = ('wide',)
    ordering = ('parent', 'title',)
    fieldsets = (
        (None, {
            'fields': (('title', 'parent', 'wide'),
                       ('content',),
                       )
        }),
    )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'40'})},
        models.TextField: {'widget': Textarea(attrs={'rows':25, 'cols':110})},
    }

admin.site.register(Page, PageAdmin)
