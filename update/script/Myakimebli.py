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

def get_myaki_mebli_matrolux():
    img_cards = []
    cards = []
    size_cards = []

    logger.info('Start ...')
    req = requests.get(File.objects.get(id=4).url, headers=HEADERS)  
    src = req.text
    logger.info('Get src ---///')
    soup = BeautifulSoup(src, 'xml')
    item = soup.find_all('entry')

    for i in item:
        try: 
            title = i.find('title').get_text() if i.find('title') else None
            product_type = i.find('product_type').get_text() if i.find('product_type') else None
            product_id = i.find('id').get_text() if i.find('id') else None
            price = str(i.find('price').get_text()).replace('.00 UAH', '') if i.find('price') else None
            description = str(i.find('description').get_text()).replace('характеристики новых шкафов: ', '') if i.find('description') else ' '
            additional_image_link = i.find('additional_image_link').get_text() if i.find('additional_image_link') else None
            image_link = i.find('image_link').get_text() if i.find('image_link') else None
            img_list = [image_link, additional_image_link]

            sale = False
            old_price = None

            subcategory = []

            if i.find('sale_price'):
                sale = True
                old_price = price
                price = str(i.find('sale_price').get_text()).replace('.00 UAH', '') if i.find('sale_price') else None
            
            
            
            if  product_type == "Дивани":
                logger.info(title)
                logger.info('-'*50)
                for cat_num in range(50):

                    if cat_num == 0:
                        cat = i.find(f'category').get_text() if i.find(f'category') else None
                    
                    else:
                        cat = i.find(f'category{cat_num}').get_text() if i.find(f'category{cat_num}') else None

                    if cat == 'Дивани':
                        subcategory.append(5)

                    if cat == 'Кутові ':
                        subcategory.append(6)

                    if cat == "Комплекти м'яких меблів":
                        subcategory.append(7)

                    if cat == 'У дитячу':
                        subcategory.append(8)

                    if cat == 'Для офісу':
                        subcategory.append(9)



                cards.append({
                    'prom':product_id,
                    'id': product_id,
                    'name': title,
                    'des':description,
                    'subcategory':subcategory
                })

                size_cards.append({
                    'id': product_id,
                    'w':'',
                    'h':'',
                    'd':'',
                    'price':price,
                    'old_price':old_price,
                    'sale':sale,
                })


                for img in img_list:
                    try:
                        img_name = img.split('/')[len(img.split('/')) - 1]
                        img_cards.append({
                            'id': product_id,
                            'img': img_name,
                            'url': img
                        })

                    except Exception as ex:
                        pass

                            
                    

        except Exception as ex:
            logger.info('-'*50)
            logger.info(ex)
            logger.info('-'*50)

    #Додаємо записи в базу
    for item in cards:
        category = Category.objects.get(id=4)
        manufacturer = 29
        external_category = 'myakimebli'
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
                        curent_price.old_price = s['old_price']
                        curent_price.sale = s['sale']
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
                    description=item['des'],
                )

                product.category.add(category)

                for sub in item['subcategory']:
                    subcategory = Subcategory.objects.get(id=sub)
                    product.subcategory.add(subcategory)

                main_price = True

                for s in size_cards:
                    if s['id'] == item['id']:

                        prace_product = ProductPrice.objects.create(
                            product=product,
                            price=s['price'],
                            old_price=s['old_price'],
                            width=s['w'],
                            height=s['h'],
                            depth=s['d'],
                            is_main=main_price,
                            sale=s['sale']
                        )

                        prace_product.save()
                        
                        main_price = False

                main_img = True

                for i in img_cards:
                    if i['id'] == item['id']:
                        try:
                            img_bytes = requests.get(i['url'], headers=HEADERS).content
                            with open(product_images_path + i['img'], "wb") as f:
                                f.write(img_bytes)

                            images_product = ProductImage.objects.create(
                                product=product,
                                image=str(i['img']),
                                is_main=main_img
                            )
                        except:
                            images_product = ProductImage.objects.create(
                                product=product,
                                image=str(i['url']),
                                is_main=main_img
                            )

                        main_img = False
                        images_product.save()

                product.save()

                logger.info('new', item['name'])

                

        except Exception as ex:
            
            logger.info(ex)
            

        

def get_myakimebli_mixmebli():
    img_cards = []
    cards = []
    size_cards = []
    url = File.objects.get(id=9).url 
    response = requests.get(url)
    categoryId = ['103',]


    logger.info('response ', response.status_code)

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        for offer in root.find('.//shop/offers').iter('offer'):
            if offer.find('categoryId').text in categoryId and offer.attrib.get('available') == 'true':
                offer_id = offer.get('id')
                logger.info(f"Offer ID: {offer_id}")

                description = offer.find('description').text
                params_html = "<table border='1'>"

                width = ''
                depth = ''
                height =''
                w_s = ''
                d_s = ''

                for param in offer.iter('param'):
                    if param.attrib.get('name') == 'Ширина':
                        width = param.text

                    if param.attrib.get('name') == 'Довжина':
                        depth = param.text
                    
                    if param.attrib.get('name') == 'Висота':
                        height = param.text

                    params_html += f"<tr><td>{param.attrib.get('name')}</td><td>{param.text}</td></tr>"
                
                params_html += "</table><br>"

                cards.append({
                    'id': offer_id,
                    'prom':offer_id,
                    'name': offer.find('name').text,
                    'des': description + params_html,
                })

                size_cards.append({
                    'id': offer_id,
                    'w':width,
                    'h':height,
                    'd':depth,
                    'w_s':w_s,
                    'd_s':d_s,
                    'price':str(offer.find('price').text).replace('.00', '')
                })

                for i in offer.findall('picture'):
                    img = str(i.text)
                    try:
                        img_name = img.split('/')[len(img.split('/')) - 1]
                        img_cards.append({
                            'id': offer_id,
                            'img': img_name,
                            'url': img
                        })

                    except Exception as ex:
                        pass
                
                logger.info(f"{offer.find('name').text} {str(offer.find('price').text).replace('.00', '')}")
                logger.info(50 * '-')


    #Додаємо записи в базу
    for item in cards:
        category = Category.objects.get(id=4)
        manufacturer = 27
        external_category = 'myakimebli'

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
                    description=item['des'],
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
                
                main_img = True

                for i in img_cards:
                    if i['id'] == item['id']:
                        try:
                            img_bytes = requests.get(i['url'], headers=HEADERS).content
                            with open(product_images_path + i['img'], "wb") as f:
                                f.write(img_bytes)

                            images_product = ProductImage.objects.create(
                                product=product,
                                image=str(i['img']),
                                is_main=main_img
                            )
                            logger.info(f"Завантажено: {i['url']}")
                        except Exception as ex:
                            images_product = ProductImage.objects.create(
                                product=product,
                                image=str(i['url']),
                                is_main=main_img
                            )
                            logger.info(ex)

                        main_img = False
                        images_product.save()

                
                logger.info('new', item['name'])

                

        except Exception as ex:
            
            logger.info(ex)



def get_myaki_mebli_yudin():
    path = File.objects.get(id=25).files
    
    logger.info(path)

    book = openpyxl.load_workbook(filename=path)
    sheet_name = ["КУТИ", "ДИВАНИ", "КОМПЛЕКТИ", "ДИТЯЧІ"]
    


    prod_id = 0
    prom = ''
    cards = []
    size_cards = []
    cell = ''

    for s in sheet_name:
        sheet = book[s]

        if s == "КУТИ":
            subcategory = 6
        
        if s == "ДИВАНИ":
            subcategory = 5

        if s == "КОМПЛЕКТИ":
            subcategory = 5

        if s == "ДИТЯЧІ":
            subcategory = 8


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
                            'subcategory':subcategory,
                        })
                    
                    logger.info((
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
        category = Category.objects.get(id=4)
        manufacturer = 28
        external_category = 'get_myaki_mebli_yudin'
        subcategory = Subcategory.objects.get(id=item['subcategory'])

        change_category(manufacturer, 'myakimebli', item['prom'], external_category)

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
                product.subcategory.add(subcategory)
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

                logger.info('new', item['name'])

                

                stock.append(product.id)

        except Exception as ex:
            
            logger.info(ex)

    #Видаляємо товар якого немає в наявності
    products = Product.objects.filter(external_category=external_category)

    for product in products:

        if product.id not in stock:
            product.delete()

            

            logger.info('Видалино: ', product.name)