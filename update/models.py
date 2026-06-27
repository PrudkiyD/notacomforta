from django.db import models
from django_ckeditor_5.fields import CKEditor5Field as RichTextField


class File(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    url = models.CharField(max_length=655, blank=True, null=True, verbose_name="Посилання")
    files = models.FileField(upload_to='files/', blank=True, null=True, verbose_name="Файл")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Прайс"
        verbose_name_plural = "Прайси"

class TaskExecution(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "В черзі"
        STARTED = "STARTED", "В процесі"
        SUCCESS = "SUCCESS", "Завершено"
        FAILED = "FAILED", "Сталася помилка"

    name = models.CharField(max_length=255, verbose_name="Назва")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name="Статус")
    result = models.TextField(null=True, blank=True, verbose_name="Результат")
    error = models.TextField(null=True, blank=True, verbose_name="Помилка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Почато")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершено")

    def __str__(self):
        return f"{self.name} ({self.status})"
    
    class Meta:
        verbose_name = "Результат оновлення"
        verbose_name_plural = "Результати оновлення"