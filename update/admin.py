from django.contrib import admin
from .models import File, TaskExecution


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('id', 'name', 'url', 'files')
    search_fields = ('name', 'url', 'files')

    class Media:
        js = ('js/update_admin.js',)

@admin.register(TaskExecution)
class TaskExecutionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "result",
        "error",
        "created_at",
        "started_at",
        "finished_at",
    )

    list_filter = (
        "status",
        "name",
        "created_at",
    )

    search_fields = (
        
        "name",
        "result",
        "error",
    )

    readonly_fields = (
        
        "name",
        "status",
        "result",
        "error",
        "created_at",
        "started_at",
        "finished_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("Основна інформація", {
            "fields": ( "name", "status")
        }),
        ("Результат", {
            "fields": ("result", "error")
        }),
        ("Час виконання", {
            "fields": ("created_at", "started_at", "finished_at")
        }),
    )

    class Media:
        js = ('js/update_admin.js',)


