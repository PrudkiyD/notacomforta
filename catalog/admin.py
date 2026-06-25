from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Manufacturer, Seria, Category, Subcategory, Product, ProductImage, ProductPrice


class SubcategoryInline(admin.StackedInline):
    model = Subcategory
    extra = 0
    verbose_name = "Підкатегорія"
    verbose_name_plural = "Підкатегорії"

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    verbose_name = "Товар"
    verbose_name_plural = "Товари"

    readonly_fields = ['get_main_price', 'editproduct', 'get_img']

    fieldsets = (
        (None, {
            'fields': ('published', 'get_img', 'name', 'manufacturer', 'category', 'subcategory', 'get_main_price', 'editproduct'),
        }),
    )

    def get_main_price(self, obj):
        price = ProductPrice.objects.filter(product=obj, is_main=True).first()

        if price:
            return mark_safe(f"<p>{price.price}</p>")
        return mark_safe("<p>Ціна не указана</p>")

    def editproduct(self, obj):
        html = f'<p><a href="/admin/catalog/product/{obj.id}/change/">Редагувати</a></p>'
        return mark_safe(html)

    def get_img(self, obj):
        # Отримання головного зображення
        img = obj.images.filter(is_main=True).first()
        html = 'Немає зображення'
        if img:
            if str(img.image.name)[0:4] == 'http':
                html = f'<img  src="{img.image.name}" style="max-height: 150px; max-width: 500px;" alt="Зображення">'
            else:
                html = f'<img  src="{img.image.url}" style="max-height: 150px; max-width: 500px;" alt="Зображення">'
            
        html += f'<br><a href="/catalog/product/{obj.id}">Переглянути на сайті</a>'

        return mark_safe(html)

    get_img.short_description = "Зображення"
    get_main_price.short_description = "Базова ціна"
    editproduct.short_description = "Редагувати товар"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display_links = ['name',]
    list_display = ['id', 'name', 'slug', 'h1']
    inlines = [SubcategoryInline]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    verbose_name = "Зображення"
    verbose_name_plural = "Зображення"

    readonly_fields = ('get_img',)

    fieldsets = (
        (None, {
            'fields': ('get_img','is_main', 'image'),
        }),
    )

    def get_img(self, obj):
        # Отримання головного зображення
        img = obj.image
        html = 'Немає зображення'
        if img:
            if str(img.name)[0:4] == 'http':
                html = f'<img  src="{img.name}" style="max-height: 150px; max-width: 150px;" alt="Зображення">'
            else:
                html = f'<img  src="{img.url}" style="max-height: 150px; max-width: 150px;" alt="Зображення">'

        return mark_safe(html)


class ProductPriceInline(admin.StackedInline):
    model = ProductPrice
    extra = 0
    verbose_name = "Ціна"
    verbose_name_plural = "Ціни"
    autocomplete_fields = ['product']

    fields = ["is_main", "sale", 
                "price", "old_price", 
                "unit", "setup", 
                "info", "width", 
                "height", "depth"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_img', 'name', 'manufacturer', 'get_categories', 'get_subcategories', 'group', 'main_price']
    list_filter = ['published', 'category', 'manufacturer',]
    search_fields = ['id', 'name', 'description', 'external_id']
    list_display_links = ['name',]
    inlines = [ProductImageInline, ProductPriceInline]
    readonly_fields =['get_img', 'slug', 'get_img_fields', "main_price", "external_id", "external_seria", "external_category", "slug"]  
    autocomplete_fields = ['manufacturer', 'seria']
    
    fieldsets = (
        ("Основна інформація", {
            "fields": ("published", "get_img_fields", "name", "description")
        }),
        ("Виробник та категорії", {
            "fields": ("manufacturer", "seria", "category", "subcategory")
        }),
        ("Додатково", {
            "fields": ("external_id", "external_seria", "external_category", "slug")
        }),
    )

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    get_categories.short_description = "Категорії"

    def get_subcategories(self, obj):
        return ", ".join([subcategory.name for subcategory in obj.subcategory.all()])
    get_subcategories.short_description = "Підкатегорії"

    def get_img(self, obj):
        # Отримання головного зображення
        img = obj.images.filter(is_main=True).first()
        html = 'Немає зображення'
        if img:
            if str(img.image.name)[0:4] == 'http':
                html = f'<img  src="{img.image.name}" style="max-height: 150px; max-width: 500px;" alt="Зображення">'
            else:
                html = f'<img  src="{img.image.url}" style="max-height: 150px; max-width: 500px;" alt="Зображення">'
            
        html += f'<br><a href="/catalog/product/{obj.id}">Переглянути на сайті</a>'

        return mark_safe(html)
    
    def get_img_fields(self, obj):
        # Отримання головного зображення
        img = obj.images.filter(is_main=True).first()
        html = 'Немає зображення'
        if img:
            if str(img.image.name)[0:4] == 'http':
                html = f'<img  src="{img.image.name}" style="max-height: 500px; max-width: 500px;" alt="Зображення">'
            else:
                html = f'<img  src="{img.image.url}" style="max-height: 500px; max-width: 500px;" alt="Зображення">'
            
        html += f'<br><a href="/catalog/product/{obj.id}">Переглянути на сайті</a>'

        return mark_safe(html)

    def main_price(self, obj):
        # Отримання головного зображення
        price = obj.prices.filter(is_main=True).first()
        html = '0'
        if price:
            # Генерація HTML для відображення зображення
            html = f'<p class="change_main_price">{price.price}</p>'

        return mark_safe(html)
    
    def group(self, obj):
        seria = obj.seria
        if seria:
            # Генерація HTML для відображення зображення
            html = f'<a href="/admin/catalog/seria/{seria.id}/change/">{seria.name}</a>'
            return mark_safe(html)
        return "-"
    
    group.short_description = "Комплект"  
    get_img.short_description = "Зображення"
    main_price.short_description = "Базова ціна"

    class Media:
        js = ('js/product_admin.js',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name']
    list_display_links = ['name',]


@admin.register(Seria)
class SeriaAdmin(admin.ModelAdmin):
    list_display_links = ['name',]
    list_display = ['id', 'name', 'manufacturer']
    search_fields = ['name']
    inlines = [ProductInline]
    list_filter = ['manufacturer',]

    fields = ['manufacturer', 'name', 'external_id', ]
   


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display_links = ['name',]
    list_display = ['id', 'name', 'slug', 'category']
    list_filter = ['category']
    list_editable = ['slug','category',]
    search_fields = ['name']

'''
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'product_id', 'is_main']
    list_filter = ['is_main']
    search_fields = ['product__name']
    ordering = ['-product_id',]


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'is_main']
    list_filter = ['is_main']
    search_fields = ['product__name']
'''