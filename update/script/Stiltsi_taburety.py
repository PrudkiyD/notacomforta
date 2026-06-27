from catalog.models import Product, ProductImage, ProductPrice, Category, Subcategory
from .Tools import HEADERS, change_category, change_category_modul, file_path, product_images_path, num_check
import xml.etree.ElementTree as ET
from update.models import File
from bs4 import BeautifulSoup
import requests
import openpyxl
import re
import logging

logger = logging.getLogger(__name__)


def get_stiltsi_taburety_modul_lux():
    path = File.objects.get(id=27).files
    logger.info(path)
    book = openpyxl.load_workbook(filename=path)
    sheet = book.worksheets[0]
    prod_id = 0
    cards = []
    size_cards = []

    for r in range(sheet.max_row):

        r += 1
        cell = str(sheet[r][0].value)
        match = re.search('Стільці', cell)

        if match:
            r = r+3
            while True:
                r += 1

                cell = str(sheet[r][0].value)
                name = str(sheet[r][1].value)
                prom = name.replace(' ', '').lower()
                size = str(sheet[r][2].value)
                try:
                    price = str(round(float(sheet[r][3].value)))
                except:
                    price = ''

                size = size.split('*')

                if price.isdigit() == False:
                    break

                else:

                    cards.append({
                        'prom': prom,
                        'id': prod_id,
                        'name': name,
                        'des': '',
                    })

                    size_cards.append({
                        'id': prod_id,
                        'w': size[0],
                        'h': size[1],
                        'd': size[2],
                        'price': price,
                    })

                    prod_id += 1
                    
                    logger.info('-'*50)
                    logger.info(prom)
                    logger.info(prod_id, name, size, price)

    
    #Додаємо записи в базу
    for item in cards:
        category = Category.objects.get(id=14)
        manufacturer = 22
        external_category = 'stiltsi_taburety'

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

                logger.info('old', product[0].name)

                

            #Додаємо новий товар
            else:
                product = Product.objects.create(
                    published=True,  
                    external_id=item['prom'],  
                    external_category=external_category,
                    manufacturer_id=manufacturer,  
                    name=item['name'],
                )

                product.category.add(category)

                product.save()

                main_price = True

                for s in size_cards:
                    if s['id'] == item['id']:

                        prace_product = ProductPrice.objects.create(
                            product=product,
                            price=s['price'],
                            width=s['w'],
                            height=s['h'],
                            depth=s['d'],
                            is_main=main_price,
                        )

                        prace_product.save()
                        
                        main_price = False

                
                logger.info('new', item['name'])

                

        except Exception as ex:
            
            logger.info(ex)