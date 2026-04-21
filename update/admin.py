from django.contrib import admin
from .models import File, History


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('id', 'name', 'url', 'files')  # Відображення у списку
    search_fields = ('name', 'url', 'files')  # Поля для пошуку

'''
@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')  # Відображення у списку
    fields = ('name', 'description', 'created_at')
    readonly_fields = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')  # Поля для пошуку
    list_filter = ('created_at',)  # Фільтрація
    ordering = ('-created_at',)  # Сортування за датою створення
'''