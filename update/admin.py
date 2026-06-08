from django.contrib import admin
from .models import File, History
from django.contrib.admin.models import LogEntry


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('id', 'name', 'url', 'files')
    search_fields = ('name', 'url', 'files')

'''
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag')
    list_filter = ('action_flag', 'content_type')
    search_fields = ('object_repr',)
    readonly_fields = fields = ('action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message')

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    fields = ('name', 'description', 'created_at')
    readonly_fields = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
'''