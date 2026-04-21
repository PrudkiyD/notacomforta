from django.db import models
from django_ckeditor_5.fields import CKEditor5Field as RichTextField

class Page(models.Model):
    published = models.BooleanField(default=True, verbose_name="Опубліковано")
    name = models.CharField(max_length=255, verbose_name="Назва")
    h1 = models.CharField(max_length=255, verbose_name="Заголовок H1")
    outside = models.BooleanField(default=False, verbose_name="Зовнішній url")
    slug = models.CharField(max_length=255, verbose_name="Slug")
    content = RichTextField(verbose_name="Контент")

    class Meta:
        verbose_name = "Сторінка"
        verbose_name_plural = "Сторінки"

    def __str__(self):
        return self.name
    

class Element(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    content = RichTextField(verbose_name="Контент")

    class Meta:
        verbose_name = "Елемент"
        verbose_name_plural = "Елементи"

    def __str__(self):
        return self.name


class Slider(models.Model):
    name = models.CharField(max_length=6200, verbose_name="Назва")
    img = models.ImageField(upload_to='slider/',verbose_name = "рекомендований розмір(1600x528)", null=True)
    url = models.CharField(max_length=255, verbose_name="Посилання")

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайдер"

    def __str__(self):
        return self.name
    
