from django import forms
from django.contrib import admin
from reversion.admin import VersionAdmin
from dmcm.cm.models import BlogPage, Page, List, Option

class BlogPageAdmin(VersionAdmin):
    list_display = ('date', 'title', 'updated')
    ordering = ('-date', 'title',)

class ListInline(admin.TabularInline):
    model = List

class PageAdmin(VersionAdmin):
    list_display = ('title', 'parent', 'updated')
    ordering = ('parent', 'title',)
    inlines = [ListInline]

class ListAdmin(VersionAdmin):
    list_display = ('title', 'parent', 'updated')
    ordering = ('parent', 'title',)

class OptionAdmin(VersionAdmin):
    list_display = ('deploy_path', 'source_dir', 'root_page', 'sitemap_list')

admin.site.register(BlogPage, BlogPageAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(Option, OptionAdmin)
