from catalog.models import Product, ProductImage, ProductPrice, Category, Subcategory
from .Tools import HEADERS, change_category, change_category_modul, file_path, product_images_path, trans, num_check
import xml.etree.ElementTree as ET
from update.models import File
from bs4 import BeautifulSoup
import requests
import time
import logging

logger = logging.getLogger(__name__)


def get_matrasy_matrolux():
    logger.info('Start ...')
    req = requests.get(File.objects.get(id=18).url,headers=HEADERS)  
    src = req.text
    logger.info(src[:500])

    soup = BeautifulSoup(src, 'xml')
    item = soup.find_all('offer')

    cards = []
    size_cards = []
    img_cards = []
    offer_list = []

    for i in item:
        name_list = str(i.find('name').get_text()).split(',')
        desc_text = '<p>' + str(i.find('description').get_text()) + '</p>'
        offer_id = i.get('group_id')
        prom = i.get('id')
        

        if offer_id not in offer_list and offer_id:
            offer_list.append(offer_id)
            picture = i.find_all('picture')
            img_list = []
            logger.info(len(offer_list), '-->', name_list[0], '-->', prom)

            for i in picture:
                img_list.append(i.get_text())

            for img_name in img_list:

                img_cards.append({
                    'id': offer_id,
                    'img': img_name,
                    'url': img_name
            })
                
                

            cards.append({
                'id': offer_id,
                'prom':prom,
                'name': name_list[0],
                'des': desc_text,
            })

            

    for i in item:
        price = i.find('price').get_text()
        oldprice = i.find('oldprice').get_text() if i.find('oldprice') else None
        size = ['', '', '']
        param_list = i.find_all('param')
        offer_id = i.get('group_id')
        option = ''

        for p in param_list:

            if p.get('name') == 'Розмір матрацу (ШхД)':
                try:
                    size[0] = p.get_text().split('x')[0]
                    size[1] = p.get_text().split('x')[1]
                except:
                    pass

            if p.get('name') == 'Тип пружинного блоку':
                try:
                    option = p.get_text()
                except:
                    pass

        size_cards.append({
                'id': offer_id,
                'option': option,
                'param': None,
                'w': size[0],
                'd': size[1],
                'price': price,
                'oldprice': oldprice,
        })

        #oldprice

    #Оновлюємо ціни
    #Додаємо записи в базу

    stock = []

    for item in cards:
        category = Category.objects.get(id=10)
        manufacturer = 23
        external_category = 'get_matrasy_matrolux'

        change_category(manufacturer, 'matrasy', item['prom'], external_category)

        try:
        #Оновлюємо ціну
            product = Product.objects.filter(
                external_id=item['prom'],
                manufacturer_id=manufacturer,
                external_category=external_category
            )

            if product.exists():
                product = product.first()
                price = ProductPrice.objects.filter(product=product).delete()

                main_price = True

                for s in size_cards:
                    sale = False

                    if s['id'] == item['id']:
                        
                        if s['oldprice']:
                            sale = True

                        prace_product = ProductPrice.objects.create(
                            product=product,
                            price=s['price'],
                            width=s['w'],
                            depth=s['d'],
                            is_main=main_price,
                            setup=s['option'],
                            old_price=s['oldprice'],
                            sale=sale
                        )

                        prace_product.save()
                        
                        main_price = False
                

                logger.info('old', product.name)

                
                
                stock.append(product.id)

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

                main_price = True

                for s in size_cards:
                    if s['id'] == item['id']:

                        if s['oldprice']:
                            sale = True

                        prace_product = ProductPrice.objects.create(
                            product=product,
                            price=s['price'],
                            width=s['w'],
                            depth=s['d'],
                            is_main=main_price,
                            setup=s['option'],
                            old_price=s['oldprice'],
                            sale=sale
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

                

                stock.append(product.id)

        except Exception as ex:
            
            logger.info(ex)


    #Видаляємо товар якого немає в наявності
    products = Product.objects.filter(external_category=external_category)

    for product in products:

        if product.id not in stock:
            product.delete()

            

            logger.info('Видалино: ', product.name)

def get_matrasy_emm():
    logger.info('Start...')

    src = requests.get(File.objects.get(id=19).url,headers=HEADERS).text
    logger.info('Get src ---///')

    soup = BeautifulSoup(src, 'xml')
    item = soup.find_all('offer')

    offer_list = []
    cards = []
    img_cards = []
    size_cards = []

    for i in item:
        offer_id = i.get('group_id')
        prom = i.get('id')
        name_list = str(i.find('name').get_text()).split('-')
        desc_text = '<p>' + str(i.find('description').get_text()) + '</p>'
        

        if offer_id not in offer_list and offer_id:
            offer_list.append(offer_id)
            picture = i.find_all('picture')
            img_list = []

            for i in picture:
                img_list.append(i.get_text())

            for i in img_list:
                img = str(i)
                img_name = img.split('/')[len(img.split('/'))-1]
                
                img_cards.append({
                    'id': offer_id,
                    'img': img_name,
                    'url': img
                })

                #logger.info(img_name)
            

            cards.append({
                'id': offer_id,
                'prom': prom,
                'name': name_list[0],
                'des': desc_text,
            })

            #logger.info(f"{prom} -> {name_list[0]}")


    for i in item:
        price = i.find('price').get_text()[:-3]

        try:
            oldprice = str(i.find('oldprice').get_text()).replace(' ', '')
            sale = True
        except:
            oldprice = None
            sale = False


        size_list = name_list = str(i.find('name').get_text()).split('-')[1]
        size = size_list.split('х')
        param_list = i.find_all('param')
        offer_id = i.get('group_id')
        option = ''

        for p in param_list:

            if p.get('name') == 'Тип пружинного блока':
                option = p.get_text()


        try:
            size = size_list.split('х')

            size_cards.append({
                'id': offer_id,
                'option': option,
                'param': '',
                'w': size[0],
                'h': '',
                'd': size[1],
                'price': price,
                'oldprice':oldprice,
                'sale':sale
            })
        except:
            size_cards.append({
                'id': offer_id,
                'option': option,
                'param': '',
                'w': '',
                'h': '',
                'd': '',
                'price': price,
                'oldprice':oldprice,
                'sale':sale
            })

        #logger.info(offer_id, '-->', option, size, price, oldprice)

    #Оновлюємо ціни
    #Додаємо записи в базу

    stock = []

    for item in cards:
        category = Category.objects.get(id=10)
        manufacturer = 15
        external_category = 'get_matrasy_emm'
        change_category(manufacturer, 'matrasy', item['prom'], external_category)

        try:
        #Оновлюємо ціну
            product = Product.objects.filter(
                external_id=item['prom'],
                manufacturer_id=manufacturer,
                external_category=external_category
            )

            if product.exists():
                product = product.first()
                price = ProductPrice.objects.filter(product=product).delete()

                main_price = True

                for s in size_cards:
                    sale = False

                    if s['id'] == item['id']:

                        prace_product = ProductPrice.objects.create(
                            product=product,
                            price=s['price'],
                            width=s['w'],
                            depth=s['d'],
                            is_main=main_price,
                            setup=s['option'],
                            old_price=s['oldprice'],
                            sale=s['sale'],
                        )

                        prace_product.save()
                        
                        main_price = False
                

                logger.info('old', product.name)

                

                stock.append(product.id)

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

                main_price = True

                for s in size_cards:
                    if s['id'] == item['id']:

                        prace_product = ProductPrice.objects.create(
                            product=product,
                            price=s['price'],
                            old_price=s['oldprice'],
                            sale=s['sale'],
                            width=s['w'],
                            height=s['h'],
                            depth=s['d'],
                            is_main=main_price,
                            setup=s['option']
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

                

                stock.append(product.id)

        except Exception as ex:
            
            logger.info(ex)

    #Видаляємо товар якого немає в наявності
    products = Product.objects.filter(external_category=external_category)

    for product in products:

        if product.id not in stock:
            product.delete()

            

            logger.info('Видалино: ', product.name)


def get_matrasy_eurosleep():
    cards = []
    img_cards = []
    size_cards = []
    prod_link = []

    # Забераємо пагенацію

    src_url_1 = File.objects.get(id=21).url
    src_url_2 = File.objects.get(id=20).url

    src = requests.get(src_url_1, headers=HEADERS)
    soup = BeautifulSoup(src.content, 'lxml')
    pag_list = [src_url_1, src_url_2]
    pagination = soup.find('ul', class_='pagination').find_all('a')

    for p in pagination:
        pag = p.get('href')
        if pag not in pag_list:
            logger.info(pag)
            pag_list.append(pag)


    src = requests.get(src_url_2, headers=HEADERS)
    soup = BeautifulSoup(src.content, 'lxml')
    pagination = soup.find('ul', class_='pagination').find_all('a')

    for p in pagination:
        pag = p.get('href')
        if pag not in pag_list:
            logger.info(pag)
            pag_list.append(pag)

    # Забераємо посилання на товар

    for url in pag_list:
        src = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(src.content, 'lxml')

        links = soup.find_all('a', class_='lazy_link')

        for l in links:
            link = l.get('href')

            if link not in prod_link:
                prod_link.append({
                    'num': len(prod_link),
                    'url': link
                })
                logger.info(len(prod_link) - 1, ':', link)

        time.sleep(3)


    for url in prod_link:

        src = requests.get(url=url['url'], headers=HEADERS)
        soup = BeautifulSoup(src.content, 'html.parser')

        name = soup.find('h1', class_='product-header').get_text()
        price_list = soup.find('div', class_='form-group required product-info-li').find_all('option')
        desc_text = soup.find('div', class_='tab-pane active')
        img_list = soup.find_all('a', class_='cloud-zoom-gallery')

        if not img_list:
            img_list = [soup.find('a', class_='cloud-zoom')]

        prom = url['url']

        logger.info(url['num'], name)

        cards.append({
            'id': url['num'],
            'prom':prom,
            'name': name,
            'des': str(desc_text),
        })

        for p in price_list:
            val = p.get('value')

            if val:
                s = p.get_text()
                s = s.replace(' ', '')
                s = s.split('(')
                size = s[0].split('х')
                price = num_check(s[1])

                try:
                    size_cards.append({
                        'id': url['num'],
                        'option': None,
                        'param': None,
                        'w': size[0],
                        'h': None,
                        'd': size[1],
                        'price': price,
                    })

                except:
                    pass

                logger.info(url['num'], size, price)
        
        for i in img_list:
            img_name = i.get('href')

            img_cards.append({
                'id': url['num'],
                'img': str(img_name).split('/')[-1],
                'url': img_name
            })
            logger.info(img_name)

        logger.info('----------------------------------------------------')
        time.sleep(1)

    #Оновлюємо ціни
    #Додаємо записи в базу
    for item in cards:
        category = Category.objects.get(id=10)
        manufacturer = 16
        external_category = 'matrasy'
        try:
        #Оновлюємо ціну
            product = Product.objects.filter(
                external_id=item['prom'],
                manufacturer_id=manufacturer,
                external_category=external_category
            )

            if product.exists():
                product = product.first()
                price = ProductPrice.objects.filter(product=product).delete()

                main_price = True

                for s in size_cards:
                    sale = False

                    if s['id'] == item['id']:

                        prace_product = ProductPrice.objects.create(
                            product=product,
                            price=s['price'],
                            width=s['w'],
                            height=s['h'],
                            depth=s['d'],
                            is_main=main_price,
                            setup=s['option']
                        )

                        prace_product.save()
                        
                        main_price = False
                

                logger.info('old', product.name)

                

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
                            setup=s['option']
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
