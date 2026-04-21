from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from catalog.models import Product, ProductPrice


class Cart(models.Model):
    customer_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Кошик"
        verbose_name_plural = "Кошики"

    def __str__(self):
        return f"Cart {self.customer_key}"


class Order(models.Model):
    customer = models.CharField(max_length=655, null=True, blank=True, verbose_name="Прізвище та ім'я")
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Номер телефону")
    coment = models.CharField(max_length=655, null=True, blank=True, verbose_name="Коментар")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата створеня")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Загальна сума")
    send = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def __str__(self):
        return f"Замовлення №{self.id}"


class CartOrderItem(models.Model):
    img = models.CharField(max_length=655, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True, blank=True)    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    coment = models.CharField(max_length=655, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    product_price = models.ForeignKey(ProductPrice, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Товар в замовленні"
        verbose_name_plural = "Товари в замовленні"
    
    def __str__(self):
        return f"{self.product.name}"
