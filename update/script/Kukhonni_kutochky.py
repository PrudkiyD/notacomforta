from catalog.models import Product, ProductImage, ProductPrice, Category, Subcategory
from .Tools import HEADERS, change_category, change_category_modul, file_path, product_images_path, num_check
import xml.etree.ElementTree as ET
from update.models import File, History
from bs4 import BeautifulSoup
import requests
import openpyxl
import re
import time


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


def get_kukhonni_kutochky_kompanit():
    type_link = [File.objects.get(id=37).url
                 ]

    pag_list = []
    prod_link = []
    cards = []
    size_cards = []
    img_cards = []

    for i in type_link:
        source = requests.get(i,headers=HEADERS).text
        soup = BeautifulSoup(source, 'html.parser')

        pag_list.append(i)
        pagination = soup.find_all('a', class_='pagination__number')

        # Забераємо пагенацію

        for p in pagination:
            pag = p.get('href')
            if pag not in pag_list and pag:
                pag_list.append(pag)
        time.sleep(1)

    # Забераємо посилання на товар

    for url in pag_list:
        source = requests.get(url,headers=HEADERS).text
        soup = BeautifulSoup(source, 'html.parser')

        links = soup.find_all('div', class_='gcell gcell--12 gcell--xs-6 gcell--md-4')

        for l in links:
            link = l.find('a').get('href')

            if link not in prod_link:
                prod_link.append({
                    'num': len(prod_link),
                    'url': link
                })

        time.sleep(1)

    # Забераємо інформацію про товар

    for url in prod_link:
        source = requests.get(url['url'],headers=HEADERS).text
        prom = url['url']
        soup = BeautifulSoup(source, 'html.parser')
        name = soup.find('h1').get_text()
        color_desc = soup.find('div', class_='item-colors')
        desc_text = soup.find('div', class_='tabs _mb-sm').get_text()
        slick = soup.find_all('a', class_='slider__slide slick-slide')
        prop_list = soup.find('div', class_='tabs _mb-sm').find_all('li')
        size = ['', '']


        print(url['url'])
        print(name)

        for i in prop_list:
            val = i.get_text()

            w_match = re.search('Ширина', val)

            d_match = re.search('Глибина', val)

            if w_match:
                size[0] = num_check(val)

            if d_match:
                size[1] = num_check(val)

        cards.append({
            'id': url['num'],
            'prom':prom,
            'name': name,
            'des': desc_text + str(color_desc),
        })

        size_cards.append({
            'id': url['num'],
            'w': size[0],
            'd': size[1],
            'price': '',
        })

        img_list = soup.find('div', class_='gcell gcell--12 gcell--def-6').find_all('a')

        for i in img_list:
            img = i.get('data-mfp-src')
            print(img)
            img_name = img.split('/')[len(img.split('/')) - 1]

            img_cards.append({
                'id': url['num'],
                'img': img_name,
                'url': img
            })

        print(size)
        print('-------------------------------')

    #Додаємо записи в базу
    
    stock = []

    for item in cards:
        category = Category.objects.get(id=15)
        manufacturer = 19
        external_category = 'get_kukhonni_kutochky_kompanit'

        change_category(manufacturer, 'komodytumby', item['prom'], external_category)

        try:
        #Оновлюємо ціну
            product = Product.objects.filter(
                external_id=item['prom'],
                manufacturer_id=manufacturer,
                external_category=external_category
            )

            if product.exists():
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

                product.category.add(category)

                main_price = True

                for s in size_cards:
                    if s['id'] == item['id']:

                        prace_product = ProductPrice.objects.create(
                            product=product,
                            price=0,
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
                        except:
                            images_product = ProductImage.objects.create(
                                product=product,
                                image=str(i['url']),
                                is_main=main_img
                            )

                        main_img = False
                        images_product.save()

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