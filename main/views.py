from django.shortcuts import render
from catalog.models import Category, Product, ProductPrice
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from page.models import Page, Slider, Element
from django.core.paginator import Paginator
import random
import xml.etree.ElementTree as ET
from datetime import datetime
from django.http import HttpResponse

def index(request):
    categorys = Category.objects.prefetch_related('subcategories')
    pages = Page.objects.filter(published=True)
    page = Page.objects.filter(slug='golovna').first()
    slider_img = Slider.objects.all()
    elements = Element.objects.all()

    products_in_category = Product.objects.filter(published=True)


    products = ProductPrice.objects.filter(product__in=products_in_category) \
        .select_related('product') \
        .prefetch_related('product__images')\
        .filter(sale=True)
    
    
    paginator = Paginator(products, 6)
    random_page = random.randint(1, paginator.num_pages)  # Випадковий номер сторінки
    page_obj = paginator.get_page(1) #random_page

    return render(request, 'main.html', {
        'title': page.h1,
        'pages':pages,
        'elements':elements,
        'products': page_obj,
        'categorys': categorys,
        'slider_img':slider_img,
        'canonical':f"https://www.notacomforta.pl.ua/"
    })


def product(request, category, id, price=None):    
    # Отримуємо товар
    item = get_object_or_404(Product, slug=f"/{category}/{id}", published=True)
    return redirect(f"/catalog/product/{item.id}")



def sitemap(request):

    id_links = [f"catalog/product/{id}" for id in Product.objects.filter(published=True).values_list('id', flat=True)]
    id_links.extend([f"catalog/{slug}" for slug in Category.objects.all().values_list('slug', flat=True)])

    # Створення кореневого елемента
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # Додавання першого URL
    url1 = ET.SubElement(urlset, "url")
    loc1 = ET.SubElement(url1, "loc")
    loc1.text = f"https://www.notacomforta.pl.ua/"
    lastmod1 = ET.SubElement(url1, "lastmod")
    lastmod1.text = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    changefreq1 = ET.SubElement(url1, "changefreq")
    changefreq1.text = "daily"
    priority1 = ET.SubElement(url1, "priority")
    priority1.text = "1.00"


    for link in id_links:
        # Додавання першого URL
        url1 = ET.SubElement(urlset, "url")
        loc1 = ET.SubElement(url1, "loc")
        loc1.text = f"https://www.notacomforta.pl.ua/{link}"
        lastmod1 = ET.SubElement(url1, "lastmod")
        lastmod1.text = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
        changefreq1 = ET.SubElement(url1, "changefreq")
        changefreq1.text = "daily"
        priority1 = ET.SubElement(url1, "priority")
        priority1.text = "1.00"



    # Перетворення XML документа у рядок
    xml_str = ET.tostring(urlset, encoding='utf-8', method='xml')
    
    # Створення HTTP відповіді з типом вмісту XML
    response = HttpResponse(xml_str, content_type='application/xml')
    return response