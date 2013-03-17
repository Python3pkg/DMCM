from django.contrib import admin
from monitoring.models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = ['level', 'datetime', 'msg']
    list_filter = ['level']
    search_fields = ['msg']
    readonly_fields = ['level', 'datetime', 'msg']
    fieldsets = (
        (None, {
            'fields': (('level', 'datetime',),
                       ('msg',),
                       )
        }),
    )
    
admin.site.register(Log, LogAdmin)
