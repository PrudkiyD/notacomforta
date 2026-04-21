from django.contrib import admin
from .models import Page, Slider, Element
from django.utils.safestring import mark_safe

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("name", "h1", "published", "outside", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "h1", "slug")
    list_filter = ("name",)

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("name", "get_img_cover", "get_url",)
    fields = ("name", "get_img", "img", "url",)
    readonly_fields = ("get_img", "get_img_cover", "get_url")

    def get_img(self, obj):
        img = obj.img.url
        html = f'<img src={img}>'
        return mark_safe(html)

    def get_img_cover(self, obj):
        img = obj.img.url
        html = f'<img src={img} style="max-width: 200px;">'
        return mark_safe(html)

    def get_url(self, obj):
        html = f'<a href="{obj.url}">{obj.url}</a>'
        return mark_safe(html)

    
    get_img.short_description = "Зображення"
    get_img_cover.short_description = "Зображення"
    get_url.short_description = "Посилання"



@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ("name",)