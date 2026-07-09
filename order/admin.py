from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Cart, Order, CartOrderItem


class CartOrderItemInline(admin.TabularInline):
    model = CartOrderItem
    extra = 0

    readonly_fields = ['get_img', 'product', 'quantity', 'product_price', ]

    fieldsets = [
    (None, {'fields': ['get_img', 'product', 'quantity', 'product_price']}),
    ]

    def get_img(self, obj):
        # Отримання головного зображення
        img = obj.img
        html = 'Немає зображення'
        if img:
            # Генерація HTML для відображення зображення
            html = (
                        f'<img  src="{img}" style="max-height: 150px; max-width: 150px;" alt="Зображення">'
                        f'<br>'
                        f'<a href="/catalog/product/{obj.product_id}">Переглянути на сайті</a>'
                    )

        return mark_safe(html)





@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'phone', 'created_at', 'total')
    search_fields = ('customer', 'phone')
    list_filter = ('created_at',)
    readonly_fields = ('customer', 'phone', 'created_at', 'coment', 'total')
    fields = ('customer', 'phone', 'coment', 'created_at', 'total')
    ordering = ('-created_at',)
    inlines = [CartOrderItemInline]

'''
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer_key', 'created_at')
    search_fields = ('customer_key',)
    inlines = [CartOrderItemInline]

    
@admin.register(CartOrderItem)
class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'product_price', 'cart', 'order')
    search_fields = ('product__name',)
    list_filter = ('cart', 'order')
'''
