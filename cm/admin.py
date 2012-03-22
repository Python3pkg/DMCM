from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput, Textarea
from dmcm.cm.models import Page
from reversion.admin import VersionAdmin

class PageAdmin(VersionAdmin):
    list_display = ('title', 'parent', 'updated')
    ordering = ('parent', 'title',)
    fieldsets = (
        (None, {
            'fields': (('title', 'parent',),
                       ('content',),
                       )
        }),
    )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'60'})},
        models.TextField: {'widget': Textarea(attrs={'rows':25, 'cols':110})},
    }

admin.site.register(Page, PageAdmin)
