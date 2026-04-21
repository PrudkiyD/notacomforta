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


class History(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    description = RichTextField(blank=True, verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = "Історія"
        verbose_name_plural = "Історія"
