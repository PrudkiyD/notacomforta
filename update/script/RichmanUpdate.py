from catalog.models import Product, ProductImage, ProductPrice, Category, Subcategory
from .Tools import HEADERS, change_category, change_category_modul, file_path, product_images_path, num_check
import xml.etree.ElementTree as ET
from update.models import File, History
from bs4 import BeautifulSoup
import random
import string
import requests
import openpyxl
import time
import re


def get_products_richman():
    paths = [File.objects.get(id=8).files, File.objects.get(id=26).files]
    
    for path in paths:

        print(path)
        book = openpyxl.load_workbook(filename=path)
        sheet = book["Ціни"]

        check_list = ['КаБаРе', 'Комфорт Плюс']
        categorys = {
                'Диван': {'id': 4},
                'Ліжко': {'id': 8},
                'КаБаРе': {'id': 14},
            }

        cards = []
        size_cards = []

        for r in range(sheet.max_row):
            r += 1
            art = sheet[r][0].value
            group = sheet[r][1].value
            name = sheet[r][2].value
            setup = sheet[r][3].value
            complect = {sheet[r][4].value}
            price_cat_1 = sheet[r][6].value
            price_cat_2 = sheet[r+1][6].value
            info = ''
            des = ''


            if complect:
                info = f"Комплектація {complect}. "

            des = f"""
                    <ul>
                        <li><b>Група:</b> {group}</li>
                        <li><b>Модефікація:</b> {setup}</li>
                        <li><b>Модефікація:</b> {info}</li>
                        <li><b>Кат.1:</b> {price_cat_1} грн.</li>
                        <li><b>Кат.2:</b> {price_cat_2} грн.</li>
                    </ul>
                    """

            if group and type(price_cat_1) == int:

                if group in check_list or setup in check_list:

                    cards.append({
                        'prom':art, 
                        'id': art,
                        'name': name,
                        'category':categorys[group]['id'],
                        'des':des
                    })

                    size_cards.append({
                        'id': art,
                        'is_main':True,
                        'setup':setup,
                        'info':f"{info}Категорія тканин 1",
                        'price':price_cat_1
                    })

                    size_cards.append({
                        'id': art,
                        'is_main':False,
                        'setup':setup,
                        'info':f"{info}Категорія тканин 2",
                        'price':price_cat_2
                    })



                    print(f"{art} {name} {group}")


    #Додаємо записи в базу

    stock = []

    for item in cards:
        manufacturer = 5
        external_category = 'get_products_richman'

        try:
        #Оновлюємо ціну
            product = Product.objects.filter(
                external_id=item['prom'],
                manufacturer_id=manufacturer,
                external_category=external_category
            )

            if product.exists():
                price = ProductPrice.objects.filter(product=product.first()).first()

                price.price = item['price']
                price.save()

                print('old', product[0].name)

                history = History.objects.create(
                            name=f"Оновлено товар",
                            description=product[0].name
                        )
                history.save()

                stock.append(product[0].id)

            #Додаємо новий товар
            else:
                product = Product.objects.create(
                    published=True,  
                    external_id=item['prom'],  
                    external_category=external_category,
                    manufacturer_id=manufacturer,  
                    name=item['name'],  
                    description=item['des'],
                )

                product.category.add(Category.objects.get(id=item['category']))

                prace_product = ProductPrice.objects.create(
                            product=product,
                            price=item['price'],
                            is_main=True,
                        )
                
                prace_product.save()
                product.save()

                print('new', item['name'])

                history = History.objects.create(
                            name=f"Додано товар",
                            description=item['name']
                        )
                history.save()

                stock.append(product.id)

        except Exception as ex:
            
            print("Помилка при оновленню товара: ", ex)
            

    #Видаляємо товар якого немає в наявності
    products = Product.objects.filter(external_category=external_category)

    for product in products:

        if product.id not in stock:
            product.delete()

            history = History.objects.create(
                            name=f"Видалино товар",
                            description=product.name
                        )
            history.save()

            print('Видалино: ', product.name)