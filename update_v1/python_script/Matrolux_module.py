import requests
import xml.etree.ElementTree as ET
import openpyxl
from bs4 import BeautifulSoup
import time
import re
import os
from googletrans import Translator
import json
from main.models import Seria, Stinka, Stinka_img
from pars.models import File




def get_stinka_matrolux():
    img_cards = []
    modul_cards = []
    product_cards = []

    print('Start m ...')
    req = requests.get('https://matroluxe.ua/index.php?route=extension/feed/ocext_feed_generator_google&token=4171&categoryview=1')  
    src = req.text
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

            if i.find('sale_price'):
                price = str(i.find('sale_price').get_text()).replace('.00 UAH', '') if i.find('sale_price') else None
            
            if  product_type == "Комплекти меблів":
                if len(str(product_id).split('-')) == 1:
                    print(f"{product_id} - {title}")
                    print('-'*50)
                    
                    vitalni = False
                    peredpokoi = False
                    spalni = False
                    dytyachi = False

                    for cat_num in range(50):
                        if cat_num == 0:
                            cat = i.find(f'category').get_text() if i.find(f'category') else None
                        
                        else:
                            cat = i.find(f'category{cat_num}').get_text() if i.find(f'category{cat_num}') else None


                        if cat == "Меблі для спальні":
                            spalni = True
                        
                        if cat == "Меблі для вітальні":
                            vitalni = True

                        if cat == "Меблі для передпокою":
                            peredpokoi = True


                    modul_cards.append({
                        'prom':product_id,
                        'id': product_id,
                        'name': title
                    })

                    product_cards.append({
                        'modul_id': product_id,
                        'prom':product_id,
                        'id': product_id,
                        'name': title,
                        'des': description,
                        'price': price,
                        'spalni':spalni,
                        'vitalni':vitalni,
                        'peredpokoi':peredpokoi,
                        'type':'STINKA'
                    })

                    
                    for img in img_list:
                        try:
                            img_name = img.split('/')[len(img.split('/')) - 1]
                            img_bytes = requests.get(img).content
                            with open("/home/ay507291/notacomforta.pl.ua/www/media/" + img_name, "wb") as f:
                                f.write(img_bytes)

                            img_cards.append({
                                'id': product_id,
                                'img': img_name
                            })
                        except:
                            pass
                    
            
            if product_type == "Корпусні меблі":
                if len(str(product_id).split('-')) == 1:
                    print(f"{product_id} - {title}")
                    print('-'*50)
                    
                    vitalni = False
                    peredpokoi = False
                    spalni = False
                    dytyachi = False

                    for cat_num in range(50):
                        if cat_num == 0:
                            cat = i.find(f'category').get_text() if i.find(f'category') else None
                        
                        else:
                            cat = i.find(f'category{cat_num}').get_text() if i.find(f'category{cat_num}') else None


                        if cat == "Меблі для спальні":
                            spalni = True
                        
                        if cat == "Меблі для вітальні":
                            vitalni = True

                        if cat == "Меблі для передпокою":
                            peredpokoi = True


                    if vitalni:

                        modul_cards.append({
                            'prom':product_id,
                            'id': product_id,
                            'name': title
                        })

                        product_cards.append({
                            'modul_id': product_id,
                            'prom':product_id,
                            'id': product_id,
                            'name': title,
                            'des': description,
                            'price': price,
                            'spalni':spalni,
                            'vitalni':vitalni,
                            'peredpokoi':peredpokoi,
                            'type':'STINKA'
                        })

                        
                        for img in img_list:
                            try:
                                img_name = img.split('/')[len(img.split('/')) - 1]
                                img_bytes = requests.get(img).content
                                with open("/home/ay507291/notacomforta.pl.ua/www/media/" + img_name, "wb") as f:
                                    f.write(img_bytes)

                                img_cards.append({
                                    'id': product_id,
                                    'img': img_name
                                })
                            except:
                                pass


            if len(str(product_id).split('-')) == 2:
                print(f"{product_id} - {title}")
                print('-'*50)

                for cat_num in range(50):
                    if cat_num == 0:
                        cat = i.find(f'category').get_text() if i.find(f'category') else None
                    
                    else:
                        cat = i.find(f'category{cat_num}').get_text() if i.find(f'category{cat_num}') else None

                    prod_type = 'OTHER'

                    if cat == "Комоди" or cat == "Тумби":
                        prod_type = 'KOMOD'
                        break
                        
                    if cat == "Шафи" or cat == "Пенали":
                        prod_type = 'SHAFI'
                        break

                    if cat == "Пуфи" or cat == "Дивани":
                        prod_type = 'OTHER'
                        break

                    if cat == "Ліжка":
                        prod_type = 'BED'
                        break
                
                modul_id = str(product_id).split('-')[0]

                product_cards.append({
                    'modul_id': modul_id,
                    'prom':product_id,
                    'id': product_id,
                    'name': title,
                    'des': description,
                    'price': price,
                    'spalni':False,
                    'vitalni':False,
                    'peredpokoi':False,
                    'type':prod_type
                })

                print(f'modul_id: {modul_id}')

                
                for img in img_list:
                    try:
                        img_name = img.split('/')[len(img.split('/')) - 1]
                        img_bytes = requests.get(img).content
                        with open("/home/ay507291/notacomforta.pl.ua/www/media/" + img_name, "wb") as f:
                            f.write(img_bytes)

                        img_cards.append({
                            'id': product_id,
                            'img': img_name
                        })

                    except:
                        pass

        except Exception as ex:
            print('-'*50)
            print(ex)
            print('-'*50)

    UpdateData(modul_cards, product_cards, img_cards, manu=3)



def UpdateData(modul_cards, product_cards, img_cards, manu):
    #Додаємо записи в базу
    new_db=[]
    for m in modul_cards:

        #Оновлюємо ціну
        if Seria.objects.filter(pars_name = m['prom']).filter(manufacturer_id=manu):
            modul_id = Seria.objects.get(pars_name = m['prom']).id
            element = Stinka.objects.filter(seria_id = modul_id)

            for el in element:
                for p in product_cards:
                    if p['prom'] == el.pars_name:
                        new_db.append(p['prom'])
                        print('old:', Stinka.objects.get(id=el.id))
                        Stinka.objects.filter(id = el.id).update(price=p['price'])

        #Додаємо новий товар
        else:
            new_id = Seria.objects.all().order_by('-id')[0].id + 1
            Seria.objects.create(id=new_id, manufacturer_id=manu, seria_name=m['name'], pars_name=m['prom'])

            for p in product_cards:
                if p['modul_id'] == m['id']:
                    new_sid = Stinka.objects.all().order_by('-id')[0].id + 1
                    Stinka.objects.create(id=new_sid, seria_id=new_id, manufacturer_id=manu,\
                                          name=p['name'], pars_name=p['prom'], categori = p['type'],\
                                            description=p['des'], price=p['price'],\
                                            spalni=p['spalni'], vitalni=p['vitalni'], peredpokoi=p['peredpokoi'])
                    new_db.append(p['prom'])
                    print('new:', p['name'])
                    
                    try:
                        for i in img_cards:
                            if i['id'] == p['id']:
                                Stinka_img.objects.get_or_create(key_img_id=new_sid, img=i['img'])
                    except:
                        pass

    #Видаляємо товар
    for m in Stinka.objects.filter(manufacturer_id=manu):
        if m.pars_name not in new_db:
            print('delet:', m)
            m.delete()

