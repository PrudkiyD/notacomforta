from catalog.models import Product, ProductImage, ProductPrice, Category, Subcategory, Seria
from .Tools import HEADERS, change_category, change_category_modul, file_path, product_images_path, num_check
import xml.etree.ElementTree as ET
from update.models import File, History
from bs4 import BeautifulSoup
import requests
from googletrans import Translator
import time


def get_stinka_matrolux():
    img_cards = []
    modul_cards = []
    product_cards = []

    print('Start m ...')
    req = requests.get(File.objects.get(id=4).url, headers=HEADERS)  
    src = req.text

    print(src)

    print('Get src m ---///')
    soup = BeautifulSoup(src, 'xml')
    item = soup.find_all('entry')

    for i in item:
        try: 
            title = i.find('title').get_text() if i.find('title') else None
            product_type = i.find('product_type').get_text() if i.find('product_type') else None
            product_id = i.find('id').get_text() if i.find('id') else None
            price = str(i.find('price').get_text()).replace('.00 UAH', '') if i.find('price') else None
            description = str(i.find('description').get_text()) if i.find('description') else ' '
            additional_image_link = i.find('additional_image_link').get_text() if i.find('additional_image_link') else None
            image_link = i.find('image_link').get_text() if i.find('image_link') else None
            img_list = [additional_image_link, image_link]
            old_price = None
            sale = False

            if i.find('sale_price'):
                old_price = price
                sale = True
                price = str(i.find('sale_price').get_text()).replace('.00 UAH', '') if i.find('sale_price') else None
            
            if  product_type == "Комплекти меблів":
                if len(str(product_id).split('-')) == 1:
                    category = None
                    

                    for cat_num in range(50):
                        if cat_num == 0:
                            cat = i.find(f'category').get_text() if i.find(f'category') else None
                        
                        else:
                            cat = i.find(f'category{cat_num}').get_text() if i.find(f'category{cat_num}') else None


                        if cat == "Меблі для спальні":
                            category = 7
                        
                        if cat == "Меблі для вітальні":
                            category = 5

                        if cat == "Меблі для передпокою":
                            category = 6

                        


                    modul_cards.append({
                        'prom':product_id,
                        'id': product_id,
                        'name': title
                    })

                    product_cards.append({
                        'modul_id': product_id,
                        'prom':product_id,
                        'id': product_id,
                        'category': category,
                        'name': title,
                        'des': description,
                        'price': price,
                        'old_price': old_price,
                        'sale': sale,
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
                    
            
            if product_type == "Корпусні меблі":
                if len(str(product_id).split('-')) == 1:

                    for cat_num in range(50):
                        if cat_num == 0:
                            cat = i.find(f'category').get_text() if i.find(f'category') else None
                        
                        else:
                            cat = i.find(f'category{cat_num}').get_text() if i.find(f'category{cat_num}') else None
                        
                        if cat == "Меблі для вітальні":

                            category = 5

                            modul_cards.append({
                                'prom':product_id,
                                'id': product_id,
                                'name': title
                            })

                            product_cards.append({
                                'modul_id': product_id,
                                'prom':product_id,
                                'id': product_id,
                                'category': category,
                                'name': title,
                                'des': description,
                                'price': price,
                                'old_price': old_price,
                                'sale': sale,
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


            if len(str(product_id).split('-')) == 2:

                for cat_num in range(50):
                    if cat_num == 0:
                        cat = i.find(f'category').get_text() if i.find(f'category') else None
                    
                    else:
                        cat = i.find(f'category{cat_num}').get_text() if i.find(f'category{cat_num}') else None

                    category = 16

                    if cat == "Комоди" or cat == "Тумби":
                        category = 11
                        break
                        
                    if cat == "Шафи" or cat == "Пенали":
                        category = 3
                        break

                    if cat == "Пуфи" or cat == "Дивани":
                        category = 4
                        break

                    if cat == "Ліжка":
                        category = 8
                        break
                
                modul_id = str(product_id).split('-')[0]

                product_cards.append({
                    'modul_id': modul_id,
                    'prom':product_id,
                    'id': product_id,
                    'category':category,
                    'name': title,
                    'des': description,
                    'price': price,
                    'old_price': old_price,
                    'sale': sale,
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
            print('-'*50)
            print(ex)
            print('-'*50)

    #Оновлення товара

    for m in modul_cards:
        manufacturer = 3
        external_category = 'get_stinka_matrolux'
        
        seria = Seria.objects.filter(external_id = m['prom'], manufacturer_id = manufacturer)

        if seria.exists():
            #Оновлюємо
            seria = seria.first()
            print(f"old: {seria.name}")

            history = History.objects.create(
                            name=f"Оновлено комплети товарів",
                            description=seria.name
                        )
            history.save()

        else:
            #Додаємо
            seria = Seria.objects(
                name=m['name'],
                external_id=m['prom'],
                manufacturer_id=manufacturer
            )
            seria.save()
            print(f"new: {m['name']}")

            history = History.objects.create(
                            name=f"Додано комплети товарів",
                            description=m['name']
                        )
            history.save()

        for p in product_cards:
                if p['modul_id'] == m['id']:
                    change_category_modul(manufacturer, 'modul', p['prom'], external_category, seria)

                    product = Product.objects.filter(external_id = p['prom'],\
                        seria = seria, manufacturer_id = manufacturer,\
                            external_category = external_category)

                    
                    if product.exists():
                        #Оновлюємо
                        product = product.first()
                        price = ProductPrice.objects.filter(product = product)

                        if price.exists():
                            price = price.first()

                            price.price = p['price']
                            price.old_price = p['old_price']
                            price.sale = p['sale']
                            price.save()

                        print(f"old: {  product.name}")

                        history = History.objects.create(
                            name=f"Оновлено товар",
                            description=product.name
                        )
                        history.save()

                    else:
                        #Додаємо
                        category = Category.objects.get(id=p['category'])

                        product = Product.objects(
                            seria=seria,
                            external_id=p['prom'],
                            manufacturer_id=manufacturer,
                            external_seria=m['prom'],
                            external_category=external_category,
                            name=p['name'],
                            description=p['des']
                        )
                        product.category.add(category)

                        price = ProductPrice.objects(
                            product=product,
                            is_main=True,
                            price=p['price'],
                            old_price=p['old_price'],
                            sale=p['sale']
                        )


                        for i in img_cards:
                            if i['id'] == p['id']:
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
                        print(f"new: {p['name']}")
                        history = History.objects.create(
                            name=f"Додано товар",
                            description=product.name
                        )
                        history.save()


        print('-'*50)