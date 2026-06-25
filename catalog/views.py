from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Product, Category, Subcategory, ProductPrice, ProductImage, Manufacturer
from page.models import Page, Element
from django.db.models import Q
import random
import re


def catalog(request):
    categorys = Category.objects.prefetch_related('subcategories')
    pages = Page.objects.filter(published=True)
    title = "Всі категорії"

    return render(request, 'all-categorys.html', {
        'title': title,
        'categorys': categorys,
        'pages':pages,
    })


def category(request, category, subcategory=None):

    categorys = Category.objects.prefetch_related('subcategories')
    pages = Page.objects.filter(published=True)
    category_obj = get_object_or_404(categorys, slug=category)  # Отримуємо категорію за slug
    title = category_obj.h1

    get_parameters = '?'
    is_main = True

    manufacturer_get = request.GET.get('manufacturer')
    width_get = request.GET.get('width')
    height_get = request.GET.get('height')
    depth_get = request.GET.get('depth')
    sort_get = request.GET.get('sort')
    

    # Отримуємо всі товари, які належать до цієї категорії
    if subcategory:
        subcategory_obj = get_object_or_404(Subcategory, slug=subcategory)
        products_in_category = Product.objects.filter(category=category_obj, subcategory=subcategory_obj, published=True)
    else:
        products_in_category = Product.objects.filter(category=category_obj, published=True)

    # Беремо список виробників
    manufacturer_list = Manufacturer.objects.filter(
                        products__in=products_in_category
                    ).values('id', 'name').distinct()

    # Фільтруємо за виробником
    if manufacturer_get and manufacturer_get != 'all':
        get_parameters += f"manufacturer={manufacturer_get}&"
        products_in_category = products_in_category.filter(manufacturer=manufacturer_get)


    products = ProductPrice.objects.filter(product__in=products_in_category) \
        .select_related('product') \
        .prefetch_related('product__images')
    
    #Беремо розміри
    width_list = products.filter(~Q(width=None), ~Q(width="None"), ~Q(width="")) \
                     .values_list('width', flat=True) \
                     .distinct() \
                     .order_by('width')
    
    
    height_list = products.filter(~Q(width=None), ~Q(width="None"), ~Q(width="")) \
                    .values_list('height', flat=True)\
                    .distinct()\
                    .order_by('height')
                    
    depth_list = products.filter(~Q(width=None), ~Q(width="None"), ~Q(width="")) \
                            .values_list('depth', flat=True)\
                            .distinct()\
                            .order_by('depth')


    # фільтруємо за розмірами
    if width_get and width_get != 'all':
        is_main = False
        get_parameters += f"width={width_get}&"
        products = products.filter(width=width_get)

    if height_get and height_get != 'all':
        is_main = False
        get_parameters += f"height={height_get}&"
        products = products.filter(height=height_get)

    if depth_get and depth_get != 'all':
        is_main = False
        get_parameters += f"depth={depth_get}&"
        products = products.filter(depth=depth_get)


    if is_main:
        products = products.filter(is_main=True)

    # Сортування за ціною
    if sort_get:
        get_parameters += f"sort={sort_get}&"
        products = products.order_by('-sale', sort_get)
    else:
        products = products.order_by('-sale', 'price')

    # Пагінація
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog.html', {
        'title': title,
        'categorys': categorys,
        'show_filter':True,
        'pages':pages,
        'products': page_obj,
        'category_slug': category,
        'page_obj': page_obj,  # Передаємо об'єкт пагінації в шаблон
        'get_parameters': get_parameters,
        'manufacturer_list':manufacturer_list,
        'width_list':width_list,
        'height_list':height_list,
        'depth_list':depth_list,
        'canonical':f"https://www.notacomforta.pl.ua/catalog/{category}"
    })


def sale(request):
    categorys = Category.objects.prefetch_related('subcategories')
    pages = Page.objects.filter(published=True)
    get_parameters = '?'

    products_in_category = Product.objects.filter(published=True)

    products = ProductPrice.objects.filter(product__in=products_in_category) \
        .select_related('product') \
        .prefetch_related('product__images')\
        .filter(sale=True)


    # Пагінація
    paginator = Paginator(products, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog.html', {
        'title': 'Знижки',
        'categorys': categorys,
        'show_filter':False,
        'pages':pages,
        'products': page_obj,
        'category_slug': category,
        'page_obj': page_obj,  # Передаємо об'єкт пагінації в шаблон
        'get_parameters': get_parameters,
        'canonical':f"https://www.notacomforta.pl.ua/catalog/sale"
    })


def search(request):
    categorys = Category.objects.prefetch_related('subcategories')
    pages = Page.objects.filter(published=True)
    get_parameters = '?'
    
    title = 'Пошук'
    q = request.GET.get('q', '').strip()
    products = []
    find_id = []
    
    
    # Фільтруємо товари за пошуковим запитом, безрегістра і символів
    if q:
        get_parameters += f"q={q}&"
        title = f'Результат пошуку: "{q}"'
        search_product = Product.objects.filter(published=True)

        for s in search_product:
            search_area = str(s.id) + str(s.name).replace(' ', '').lower()
            q = str(q).lower()

            if re.search(q, search_area):
                find_id.append(s.id)

        

    products = ProductPrice.objects.filter(
        product_id__in=find_id, 
        is_main=True
    ).select_related('product').prefetch_related('product__images')
    

    # Пагінація
    paginator = Paginator(products, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'catalog.html', {
        'title': title,
        'categorys': categorys,
        'show_filter': False,
        'pages': pages,
        'products': page_obj,
        'category_slug': None,
        'page_obj': page_obj,
        'get_parameters': get_parameters,
    })


def product(request, product_id, price=None):
    categorys = Category.objects.prefetch_related('subcategories')
    elements = Element.objects.all()
    pages = Page.objects.filter(published=True)

    
    # Отримуємо товар
    try:
        item = get_object_or_404(Product, id=product_id, published=True)
    except (ValueError, TypeError):
        raise Http404()

    if price:
        prices = item.prices.order_by('is_main')
    else:
        prices = item.prices.order_by('-is_main')



    products_in_category = Product.objects.filter(published=True, category__in=item.category.all())

    sale_products = ProductPrice.objects.filter(product__in=products_in_category) \
        .select_related('product') \
        .prefetch_related('product__images')\
        .filter(sale=True)

    group_product = False
    if item.seria:
        products_in_group = Product.objects.filter(seria=item.seria, manufacturer=item.manufacturer)

        group_product = ProductPrice.objects.filter(product__in=products_in_group) \
            .select_related('product') \
            .prefetch_related('product__images')\
            .filter(is_main=True)
    

    sale_products = sale_products.order_by('id')
    paginator = Paginator(sale_products, 8)
    page_obj = paginator.get_page(1)

    try:
        imgseo = item.images.filter(is_main=True).first().image
    except:
        imgseo = ''

    return render(request, 'product-page.html', {
        'title': item.name,
        'item':item,
        'prices':prices,
        'elements':elements,
        'categorys': categorys,
        'show_filter': False,
        'pages': pages,
        'sale_products': page_obj,
        'group_product': group_product,
        'imgseo':imgseo,
        'canonical':f"https://www.notacomforta.pl.ua/catalog/product/{item.id}"
    })