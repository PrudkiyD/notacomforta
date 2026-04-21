import requests
import xml.etree.ElementTree as ET
import openpyxl
from bs4 import BeautifulSoup
import csv
import time
import re
import os
import json
from kukhonni_kutochky.models import Kukhonni_kutochky, Kukhonni_kutochky_size, Kukhonni_kutochky_img
from pars.models import File


with open('/home/ay507291/notacomforta.pl.ua/www/pars/src.json', 'r') as f:
    file = json.load(f)

path_dirver = file['src'][0]['path_dirver']
accept = file['src'][1]['accept']
user_agent = file['src'][2]['user-agent']

HEADERS = {
    'accept': accept,
    'user-agent': user_agent
}


def num_check(text):
    num = ''
    for t in str(text):
        if t.isdigit():
            num += t
    return num


def get_kukhonni_kutochky_kompanit():
    type_link = ['https://kompanit.com.ua/catalog/kuhonni-kutochki/c10'
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
            img_bytes = requests.get(img).content
            with open("/home/ay507291/notacomforta.pl.ua/www/media/" + img_name, "wb") as f:
                f.write(img_bytes)

            img_cards.append({
                'id': url['num'],
                'img': img_name
            })

            print(img_name)

        print(size)
        print('-------------------------------')

    #Додаємо записи в базу
    new_db=[]
    for product in cards:
        print('------------------------------------------------')
        product['name']
        try:
            #Оновлюємо ціну
            if Kukhonni_kutochky.objects.filter(pars_name = product['prom']):
                print('old', Kukhonni_kutochky.objects.get(pars_name=product['prom']).name)
                model_id =  Kukhonni_kutochky.objects.get(pars_name=product['prom']).id
                size_id = Kukhonni_kutochky_size.objects.filter(kukhonni_kutochky_id=model_id).values()[0]['id']
                new_db.append(product['prom'])
                '''for s in size_cards:
                    if s['id'] == product['id']:
                        Kukhonni_kutochky_size.objects.filter(id = size_id).update(price=s['price'])'''
                
            #Додаємо новий товар
            else:
                new_id = Kukhonni_kutochky.objects.all().order_by('-id')[0].id + 1
                new_db.append(product['prom'])
                Kukhonni_kutochky.objects.get_or_create(id=new_id, manufacturer_id=19, name=product['name'],\
                    pars_name=product['prom'], description=product['des'])
                
                for s in size_cards:
                    if s['id'] == product['id']:
                        Kukhonni_kutochky_size.objects.get_or_create(kukhonni_kutochky_id=new_id,\
                            w=s['w'], d=s['d'], price=s['price'])

                for i in img_cards:
                    if i['id'] == product['id']:
                        Kukhonni_kutochky_img.objects.get_or_create(key_img_id=new_id, img=i['img'])


                print('new', new_id, product['name'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')

    #Видаляємо товар
    for m in Kukhonni_kutochky.objects.filter(manufacturer_id=19):
        print(m)
        if m.pars_name not in new_db:
            print('delet:', m)
            m.delete()


def get_kukhonni_kutochky_lion():
    path ="/home/ay507291/notacomforta.pl.ua/www"+File.objects.get(id=7).file_up.url
    print(path)
    book = openpyxl.load_workbook(filename=path)
    sheet = book.worksheets[1]
    cards = []
    size_cards = []
    prod_id = 0

    for r in range(sheet.max_row):
        r += 1
        cell = str(sheet[r][1].value)
        match = re.search('Кухонні кутки', cell)

        if match:
            while True:
                r += 1
                name = str(sheet[r][1].value)

                match = re.search("Дивани", name)

                if match:
                    break

                elif name != 'None':

                    try:
                        name = " ".join(name.split())
                        size = str(sheet[r][3].value)
                        size = size.split('х')
                        try:
                            price = round(int(sheet[r][5].value))
                        except:
                            price = round(int(sheet[r][8].value))


                        prod_id += 1

                        cards.append({
                            'id': prod_id,
                            'name': name,
                            'des': '',
                        })

                        size_cards.append({
                            'id': prod_id,
                            'w': size[0],
                            'd': size[1],
                            'price': price,
                        })

                        print(prod_id, name.replace('  ', ''), size, price)
                    except Exception as ex:
                        print(ex)
                        break



    #Додаємо записи в базу
    new_db=[]
    for product in cards:
        print('------------------------------------------------')
        product['name']
        try:
            #Оновлюємо ціну
            if Kukhonni_kutochky.objects.filter(pars_name = product['name']):
                print('old', Kukhonni_kutochky.objects.get(pars_name=product['name']).name)
                model_id =  Kukhonni_kutochky.objects.get(pars_name=product['name']).id
                size_id = Kukhonni_kutochky_size.objects.filter(kukhonni_kutochky_id=model_id).values()[0]['id']
                new_db.append(product['name'])
                for s in size_cards:
                    if s['id'] == product['id']:
                        
                        Kukhonni_kutochky_size.objects.filter(id = size_id).update(price=s['price'])
                
            #Додаємо новий товар
            else:
                new_id = Kukhonni_kutochky.objects.all().order_by('-id')[0].id + 1
                new_db.append(product['name'])
                Kukhonni_kutochky.objects.get_or_create(id=new_id, manufacturer_id=6, name=product['name'],\
                    pars_name=product['name'], description=product['des'])
                
                for s in size_cards:
                    if s['id'] == product['id']:
                        Kukhonni_kutochky_size.objects.get_or_create(kukhonni_kutochky_id=new_id,\
                            w=s['w'], d=s['d'], price=s['price'])

                print('new', new_id, product['name'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')

    #Видаляємо товар
    for m in Kukhonni_kutochky.objects.filter(manufacturer_id=6):
        print(m)
        if m.pars_name not in new_db:
            print('delet:', m)
            m.delete()


def get_kukhonni_kutochky_mixmebli():
    img_cards = []
    cards = []
    size_cards = []
    url = 'https://baustoff.com.ua/data/yml_mixmebli.xml'
    response = requests.get(url)
    categoryId = ['102',]


    print('response ', response.status_code)

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        for offer in root.find('.//shop/offers').iter('offer'):
            if offer.find('categoryId').text in categoryId and offer.attrib.get('available') == 'true':
                try:
                    offer_id = offer.get('id')
                    print(f"Offer ID: {offer_id}")

                    description = offer.find('description').text
                    params_html = "<table border='1'>"

                    width = ''
                    depth = ''
                    height =''

                    for param in offer.iter('param'):
                        if param.attrib.get('name') == 'Ширина':
                            width = param.text

                        if param.attrib.get('name') == 'Глибина':
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
                        'd':depth,
                        'price':str(offer.find('price').text).replace('.00', '')
                    })

                    for i in offer.findall('picture'):
                        img = str(i.text)
                        img_name = img.split('/')[len(img.split('/')) - 1]
                        img_bytes = requests.get(img).content
                        with open("/home/ay507291/notacomforta.pl.ua/www/media/" + img_name, "wb") as f:
                            f.write(img_bytes)

                        img_cards.append({
                            'id': offer_id,
                            'img': img_name
                        })
                    
                    print('------------------------------------')
                
                except Exception as ex:
                    print(ex)
    
    #Додаємо записи в базу
    new_db=[]
    for product in cards:
        print('------------------------------------------------')
        product['name']
        try:
            #Оновлюємо ціну
            if Kukhonni_kutochky.objects.filter(pars_name = product['prom']):
                print('old', Kukhonni_kutochky.objects.get(pars_name=product['prom']).name)
                model_id =  Kukhonni_kutochky.objects.get(pars_name=product['prom']).id
                size_id = Kukhonni_kutochky_size.objects.filter(kukhonni_kutochky_id=model_id).values()[0]['id']
                new_db.append(product['prom'])
                for s in size_cards:
                    if s['id'] == product['id']:
                        Kukhonni_kutochky_size.objects.filter(id = size_id).update(price=s['price'])
                
            #Додаємо новий товар
            else:
                new_id = Kukhonni_kutochky.objects.all().order_by('-id')[0].id + 1
                new_db.append(product['prom'])
                Kukhonni_kutochky.objects.get_or_create(id=new_id, manufacturer_id=27, name=product['name'],\
                    pars_name=product['prom'], description=product['des'])
                
                for s in size_cards:
                    if s['id'] == product['id']:
                        Kukhonni_kutochky_size.objects.get_or_create(kukhonni_kutochky_id=new_id,\
                            w=s['w'], d=s['d'], price=s['price'])

                for i in img_cards:
                    if i['id'] == product['id']:
                        Kukhonni_kutochky_img.objects.get_or_create(key_img_id=new_id, img=i['img'])


                print('new', new_id, product['name'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')

    #Видаляємо товар
    for m in Kukhonni_kutochky.objects.filter(manufacturer_id=27):
        print(m)
        if m.pars_name not in new_db:
            print('delet:', m)
            m.delete()

