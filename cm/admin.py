from django.contrib import admin
from reversion.admin import VersionAdmin
from dmcm.cm.models import Page

class PageAdmin(VersionAdmin):
    list_display = ('title', 'parent', 'updated')
    ordering = ('parent', 'title',)

admin.site.register(Page, PageAdmin)
