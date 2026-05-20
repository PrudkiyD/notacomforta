from django.db import models
from django_ckeditor_5.fields import CKEditor5Field as RichTextField
from django.utils.text import slugify


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Виробник")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Виробник"
        verbose_name_plural = "Виробники"


class Seria(models.Model):
    name = models.CharField(max_length=255, verbose_name="Серія")
    external_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="Зовнішній ID")
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True, on_delete=models.CASCADE, related_name='seria', verbose_name="Виробник")
    def __str__(self):
        return f"{self.id} {self.name}"

    class Meta:
        verbose_name = "Комплет товарів"
        verbose_name_plural = "Комплети товарів"


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категорія")
    h1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Заголовок h1")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="Слаг")
    image = models.FileField(upload_to='icone/', blank=True, null=True, verbose_name="Зображення")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Subcategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Підкатегорія")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Категорія")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="Слаг")
    image = models.ImageField(upload_to='icone/', blank=True, null=True, verbose_name="Зображення")

    def __str__(self):
        return f'{self.category.name} / {self.name}'

    class Meta:
        verbose_name = "Підкатегорія"
        verbose_name_plural = "Підкатегорії"


class Product(models.Model):
    published = models.BooleanField(default=False, verbose_name="Опубліковано")
    external_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="Зовнішній ID")
    external_seria = models.CharField(max_length=255, blank=True, null=True, verbose_name="Зовнішній ID серії")
    external_category = models.CharField(max_length=255, blank=True, null=True, verbose_name="Зовнішня категорія")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='products', verbose_name="Виробник")
    seria = models.ForeignKey(Seria, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Серія")
    category = models.ManyToManyField(Category, related_name='products', verbose_name="Категорія")
    subcategory = models.ManyToManyField(Subcategory, blank=True, related_name='products', verbose_name="Підкатегорія")
    name = models.CharField(max_length=255, verbose_name="Назва товару")
    description = RichTextField(blank=True, verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    slug = models.CharField(max_length=255, blank=True, null=True, verbose_name="Попередній url")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Товар")
    image = models.ImageField(verbose_name="Зображення")
    is_main = models.BooleanField(default=False, verbose_name="Головне зображення")

    def __str__(self):
        return f"{self.image.name}"

    class Meta:
        verbose_name = "Зображення товару"
        verbose_name_plural = "Зображення товарів"


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices', verbose_name="Товар")
    sale = models.BooleanField(default=False, verbose_name="Знижка")
    price = models.IntegerField(verbose_name="Ціна")
    old_price = models.IntegerField(verbose_name="Стара ціна", blank=True, null=True,)
    unit = models.CharField(default='грн.', max_length=255, blank=True, null=True, verbose_name="Одиниці")
    is_main = models.BooleanField(default=False, verbose_name="Базова ціна")
    setup = models.CharField(max_length=255, blank=True, null=True, verbose_name="Сетап")
    info = models.CharField(max_length=255, blank=True, null=True, verbose_name="Інформація")
    width = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ширина")
    height = models.CharField(max_length=255, blank=True, null=True, verbose_name="Висота")
    depth = models.CharField(max_length=255, blank=True, null=True, verbose_name="Довжина/Глибина")

    def __str__(self):
        text = ''

        if self.width:
            text += f"Ширина: {self.width} "
        
        if self.height:
            text += f"Висота: {self.height} "

        if self.depth:
            text += f"Довжина: {self.depth} "

        if self.price:
            text += f"Ціна: {self.price}"

        return text

    class Meta:
        verbose_name = "Ціна товару"
        verbose_name_plural = "Ціни товарів"
