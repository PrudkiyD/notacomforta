from catalog.models import Product, ProductImage, ProductPrice, Category, Subcategory
from .Tools import HEADERS, change_category, change_category_modul, file_path, product_images_path, num_check
import xml.etree.ElementTree as ET
from update.models import File, History
from bs4 import BeautifulSoup
import requests
import openpyxl
import re


def get_kukhonni_kutochky_yudin():
    path = File.objects.get(id=25).files
    
    print(path)

    book = openpyxl.load_workbook(filename=path)
    sheet_name = ["КУХОННІ",]
    


    prod_id = 0
    prom = ''
    cards = []
    size_cards = []
    cell = ''

    for s in sheet_name:
        sheet = book[s]

        for r in range(sheet.max_row):
            r += 1

            check = cell
            cell = sheet[r][1].value

            if check == "Назва" and cell != "Назва":

                if cell:
            
                    name = str(sheet[r][1].value).replace('\n', ' ').replace('  ', '')
                    price_list = [
                        sheet[r][2].value,
                        sheet[r][3].value,
                        sheet[r][4].value,
                        sheet[r][5].value,
                        sheet[r][6].value,
                    ]

                    prom = name.replace(' ', '').replace('\t', '').lower()

                    cards.append({
                            'id': prod_id,
                            'prom':prom,
                            'name': name,
                        })
                    
                    print((
                        f'{prod_id}: {prom}\n'
                        f'Назва: {name}\n'
                    ))
                        
                    
                    tkan = 0
                    
                    for price in price_list:

                        if price:
                            size_cards.append({
                                'id': prod_id,
                                'info': f"Категорія тканини: {tkan}" ,
                                'price': num_check(price)
                            })

                            tkan += 1
                    

                    prod_id += 1
                    cell = "Назва"


    #Додаємо записи в базу

    stock = []

    for item in cards:
        category = Category.objects.get(id=15)
        manufacturer = 28
        external_category = 'get_kukhonni_kutochky_yudin'

        change_category(manufacturer, 'kukhonni_kutochky', item['prom'], external_category)

        try:
        #Оновлюємо ціну
            product = Product.objects.filter(
                external_id=item['prom'],
                manufacturer_id=manufacturer,
                external_category=external_category
            )

            if product.exists():
                price = ProductPrice.objects.filter(product=product.first())
                index = 0

                for s in size_cards:
                    if s['id'] == item['id']:
                        curent_price = price[index]
                        curent_price.price = s['price']
                        curent_price.save()

                        index += 1

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
                    published=False,  
                    external_id=item['prom'],  
                    external_category=external_category,
                    manufacturer_id=manufacturer,  
                    name=item['name'],  
                )

                product.category.add(category)
                main_price = True

                for s in size_cards:
                    if s['id'] == item['id']:

                        prace_product = ProductPrice.objects.create(
                            product=product,
                            price=s['price'],
                            is_main=main_price,
                            info=s['info']
                        )

                        prace_product.save()
                        
                        main_price = False

                product.save()

                print('new', item['name'])

                history = History.objects.create(
                            name=f"Додано товар",
                            description=item['name']
                        )
                history.save()

                stock.append(product.id)

        except Exception as ex:
            
            print(ex)
    
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