from django.http import HttpResponse, JsonResponse
import requests
from django.shortcuts import redirect
import re
import time
from bs4 import BeautifulSoup
import urllib.parse
from .models import Manufacturer, Seria, Product, ProductImage, ProductPrice, Category, Subcategory
from PIL import Image

HEADERS = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"
}

product_images_path = r"E:\back\app\media\product_images\\"
files_path = r"E:\back\app\media\files\\"

def import_data(request):
    if not request.user.is_superuser:
        return redirect('/admin')
    
    url = "https://www.notacomforta.pl.ua/kyhni/export/manufacturer/json"
    response = requests.get(url, headers=HEADERS)

    data = response.json()
    for item in data:
        manufacturer = Manufacturer.objects.create(
            **item
        )

        manufacturer.save()
    

    
    url = "https://www.notacomforta.pl.ua/export/seria/json"
    response = requests.get(url, headers=HEADERS)

    data = response.json()
    for item in data:
        seria = Seria.objects.create(
            **item
        )

        seria.save()

    
    urls = [
        "https://www.notacomforta.pl.ua/kyhni/export/kyhni/json",
        "https://www.notacomforta.pl.ua/shafi/export/shafi/json",
        "https://www.notacomforta.pl.ua/myakimebli/export/myakimebli/json",
        "https://www.notacomforta.pl.ua/lizhka/export/lizhka/json",
        "https://www.notacomforta.pl.ua/matrasy/export/matrasy/json",
        "https://www.notacomforta.pl.ua/komodytumby/export/komodytumby/json",
        "https://www.notacomforta.pl.ua/stoly/export/stoly/json",
        "https://www.notacomforta.pl.ua/pcstoly/export/pcstoly/json",
        "https://www.notacomforta.pl.ua/stiltsi_taburety/export/stiltsi_taburety/json",
        "https://www.notacomforta.pl.ua/kukhonni_kutochky/export/kukhonni_kutochky/json",
        "https://www.notacomforta.pl.ua/dribnytsi/export/dribnytsi/json",
        "https://www.notacomforta.pl.ua/export/stinka/json"
        ]
    

    for url in urls:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            return HttpResponse(f'<h1>Помилка завантаження даних: {response.status_code}</h1>')

        data = response.json()
    
        for item in data:

            cat = url.split('/')

            print(item.get('name', "Без назви"))

            
            product = Product.objects.create(
                published=item.get('published', False),  
                external_id=item.get('external_id', None),  
                external_seria=item.get('external_seria', None),
                external_category=item.get('external_category', None),
                manufacturer_id=item.get('manufacturer_id', None),  
                seria_id=item.get('seria_id', None),
                name=item.get('name', "Без назви"),  
                slug=item.get('slug', None), 
                description=item.get('description', None)
            )

            for cat in item['category']:
                if cat:
                    category = Category.objects.get(id=cat)
                    product.category.add(category)

            for subcat in item['subcategory']:
                if subcat:
                    subcategory = Subcategory.objects.get(id=subcat)
                    product.subcategory.add(subcategory)

            
            

            for price in item['prices']:
                prace_product = ProductPrice.objects.create(
                    product=product,
                    sale=price.get('sale', False),
                    price=price.get('price', 0),
                    old_price=price.get('old_price', 0),
                    is_main=price.get('is_main', False),
                    setup=price.get('setup', None),
                    info=price.get('info', None),
                    width=price.get('width', None),
                    height=price.get('height', None),
                    depth=price.get('depth', None),
                )

                prace_product.save()

            for image in item['images']:
                images_product = ProductImage.objects.create(
                    product=product,
                    image=image.get('image', None),
                    is_main=image.get('is_main', False)
                )

                images_product.save()

            product.save()
            
    

    return HttpResponse('<h1>Дані імпортовано успішно!</h1>')


def delete(request):
    if not request.user.is_superuser:
        return redirect('/admin')
    Product.objects.all().delete()
    ProductImage.objects.all().delete()
    ProductPrice.objects.all().delete()
    Manufacturer.objects.all().delete()
    Seria.objects.all().delete()
    return HttpResponse('<h1>Дані видалено успішно!</h1>')


def img(request):
    if not request.user.is_superuser:
        return redirect('/admin')
    image = ProductImage.objects.all()
    for item in image:
        img = urllib.parse.unquote(str(item.image).replace('/media/product_images/', ''))
        # Виправляємо відсутній слеш у "https:/"
        if img.startswith("https:/") and not img.startswith("https://"):
            img = img.replace("https:/", "https://", 1)

        if re.search(r'^https://', img):  # Перевіряємо правильний формат
            print(img)

            img_name = img.split('/')[len(img.split('/')) - 1]
            img_bytes = requests.get(img, headers=HEADERS).content
            with open(product_images_path + img_name, "wb") as f:
                f.write(img_bytes)


            item.image = f"/media/product_images/{img_name}"
            item.save()

            
            
    return HttpResponse('<h1>Зображення завантажено!</h1>')


def imgdes(request):
    if not request.user.is_superuser:
        return redirect('/admin')
    product = Product.objects.all()

    source = ''

    for prod in product:
        source += prod.description

    soup = BeautifulSoup(source, 'html.parser')

    print(source)

    return HttpResponse('<h1>Зображення з описа завантажено!</h1>')


def editimg(request):
    if not request.user.is_superuser:
        return redirect('/admin')
    
    for img in ProductImage.objects.all():
        name = str(img.image).split('/')

        if name[2][0:4] == 'http':
            img.image = str(img.image).removeprefix('/media/')
            img.save()

    return HttpResponse(f'<h1>Зображення відредаговано</h1>')


def editimgmedia(request):
    if not request.user.is_superuser:
        return redirect('/admin')
    
    for img in ProductImage.objects.all():
        name = str(img.image)

        if name[0:7] == '/media/':
            img.image = str(img.image).removeprefix('/media/')
            img.save()

    return HttpResponse(f'<h1>Зображення відредаговано</h1>')


def matras(request):
    cat = Category.objects.get(id=10)
    product = Product.objects.filter(category=cat, manufacturer_id=23)

    for p in product:
        prices = p.prices.all()

        for price in prices:
            price.info = ''
            price.save()

    product = Product.objects.filter(category=cat, manufacturer_id=15)

    for p in product:
        prices = p.prices.all()

        for price in prices:
            price.info = ''
            price.save()
            

    return HttpResponse(f'<h1>Матраси відредаговано</h1>')


def editkyhni(request):
    cat = Category.objects.get(id=2)
    product = Product.objects.filter(category=cat,)

    for p in product:
        prices = p.prices.all()

        print(p.name)

        for price in prices:
            price.unit = 'грн/м.пог'
            price.save()
    return HttpResponse(f'<h1>Кухні відредаговано</h1>')


def edithttp(request):
    if not request.user.is_superuser:
        return redirect('/admin')
    
    for img in ProductImage.objects.all():
        name = str(img.image)

        if name[0:4] == 'http':
            name = name.replace('https%3A/', 'https://')
            img.image = name
            img.save()
            print(name)

    return HttpResponse(f'<h1>Зображення відредаговано</h1>')


def encodedimg(request):
    if not request.user.is_superuser:
        return redirect('/admin')
    
    for img in ProductImage.objects.all():
        if '%' in img.image.name:  # Перевіряємо, чи є в імені закодовані символи
            name = urllib.parse.unquote(img.image.name)
            img.image = name
            img.save()
        else:
            name = img.image.name

        print(name)

    return HttpResponse('<h1>Зображення відредаговано</h1>')


def shafi(request):
    if not request.user.is_superuser:
        return redirect('/admin')
    
    cat = Category.objects.get(id=3)
    products = Product.objects.filter(category=cat, manufacturer_id=3)

    
    for product in products:
        images = product.images.all()

        try:
            new = images[1]
            new.is_main = True
            new.save()
        
            main_img = images[0]
            main_img.is_main = False
            main_img.save()

            
        except:
            pass

    return HttpResponse('<h1>Шафи відредаговано</h1>')


def convertimg(request):
    if not request.user.is_superuser:
        return redirect('/admin')
    
    input_path = 'media/irish-ts-liy-png-9.png'
    output_path = 'media/irish-ts-liy-png-9.webp'

    image = Image.open(input_path)
    image.save(output_path, 'webp', quality=80)
    print(f"Converted: {input_path} -> {output_path}")
    
    return HttpResponse('<h1>Конвертація</h1>')


def test(request):
    if not request.user.is_superuser:
        return redirect('/admin')


    category = Category.objects.get(id=8)
    manufacturer = Manufacturer.objects.get(id=2)
    products = Product.objects.filter(category=category, manufacturer=manufacturer)

    for p in products:
        p.external_id = str(p.external_id).replace(' ', '').lower()
        p.save()


    source = 'test'

    return HttpResponse(f'<h1>{source}</h1>')    