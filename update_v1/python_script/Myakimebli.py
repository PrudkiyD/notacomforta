import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import openpyxl
import json
import re
from myakimebli.models import Myakimebli, Myakimebli_img, Product_myakimebli
from pars.models import File
from django.db.models import Q


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


foto_link = []


def get_myaki_mebli_matrolux():
    img_cards = []
    cards = []
    size_cards = []

    print('Start ...')
    req = requests.get('https://matroluxe.ua/index.php?route=extension/feed/ocext_feed_generator_google&token=4171&categoryview=1', headers=HEADERS)  
    src = req.text
    print('Get src ---///')
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

            if i.find('sale_price'):
                sale = True
                old_price = price
                price = str(i.find('sale_price').get_text()).replace('.00 UAH', '') if i.find('sale_price') else None
            
            
            
            if  product_type == "Дивани":
                if len(str(product_id).split('-')) == 1:
                    print(title)
                    print('-'*50)
                    for cat_num in range(50):
                        dyvany = False
                        kytovi = False
                        komplekty = False
                        dytyachi = False
                        ofis = False

                        if cat_num == 0:
                            cat = i.find(f'category').get_text() if i.find(f'category') else None
                        
                        else:
                            cat = i.find(f'category{cat_num}').get_text() if i.find(f'category{cat_num}') else None

                        if cat == 'Дивани':
                            dyvany = True

                        if cat == 'Кутові ':
                            kytovi = True

                        if cat == "Комплекти м'яких меблів":
                            komplekty = True

                        if cat == 'У дитячу':
                            dytyachi = True

                        if cat == 'Для офісу':
                            ofis = True



                    cards.append({
                        'prom':product_id,
                        'id': product_id,
                        'name': title,
                        'des':description,
                        'sale':sale,
                        'dyvany':dyvany,
                        'kytovi':kytovi,
                        'komplekty':komplekty,
                        'dytyachi':dytyachi,
                        'ofis':ofis
                    })

                    size_cards.append({
                        'id': product_id,
                        'w':'',
                        'h':'',
                        'd':'',
                        'price':price,
                        'old_price':old_price,
                    })


                    for img in img_list:
                        print(f"img---{img}---///")
                        try:
                            img_name = img.split('/')[len(img.split('/')) - 1]
                            img_bytes = requests.get(img, headers=HEADERS).content
                            with open("/home/ay507291/notacomforta.pl.ua/www/media/" + img_name, "wb") as f:
                                f.write(img_bytes)

                            img_cards.append({
                                'id': product_id,
                                'img': img_name
                            })

                        except Exception as ex:
                            print(f'///-------{ex}---------///')

                            
                    

        except Exception as ex:
            print('-'*50)
            print(ex)
            print('-'*50)

    '''
    for product in cards:
        queryset = Myakimebli.objects.filter(pars_name=product['name'])
        if queryset.exists():
            queryset.update(pars_name=product['prom'])'''

    
    #Додаємо записи в базу
    new_db=[]
    for product in cards:
        print('------------------------------------------------')
        product['name']
        try:
            #Оновлюємо ціну
            if Myakimebli.objects.filter(pars_name = product['prom']):
                print('old', product['name'])
                model_id =  Myakimebli.objects.get(pars_name=product['prom']).id
                Myakimebli.objects.filter(id = model_id).update(sale = product['sale'])
                size_id = Product_myakimebli.objects.filter(myakimebli_name_id=model_id).values()[0]['id']
                new_db.append(product['prom'])

                for s in size_cards:
                    if s['id'] == product['id']:
                        Product_myakimebli.objects.filter(id = size_id).update(price=s['price'], old_price=s['old_price'])
                        break
                
            #Додаємо новий товар
            else:
                new_id = Myakimebli.objects.all().order_by('-id')[0].id + 1
                new_db.append(product['prom'])
                Myakimebli.objects.get_or_create(id=new_id, manufacturer_id=29, myakimebli_name=product['name'],\
                    pars_name=product['prom'], description=product['des'],\
                        dyvany=product['dyvany'], kytovi=product['kytovi'], komplekty=product['komplekty'],\
                            dytyachi=product['dytyachi'], ofis=product['ofis'])
                
                for s in size_cards:
                    if s['id'] == product['id']:
                        Product_myakimebli.objects.get_or_create(myakimebli_name_id=new_id,\
                                                                 price=s['price'], old_price=s['old_price'])

                for i in img_cards:
                    if i['id'] == product['id']:
                        Myakimebli_img.objects.get_or_create(myakimebli_img_id=new_id, img=i['img'])


                print('new', new_id, product['prom'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')

    #Видаляємо товар
    for m in Myakimebli.objects.filter(manufacturer_id=29):
        if m.pars_name not in new_db:
            print('delet:', m)
            m.delete()

    


def get_products_richman():
    path ="/home/ay507291/notacomforta.pl.ua/www"+File.objects.get(id=5).file_up.url
    book = openpyxl.load_workbook(filename=path)
    sheet = book["Ціни"]

    prod_id = 0
    check_name = ''
    prom = ''
    cards = []
    size_cards = []

    print("Start...")

    for r in range(sheet.max_row):
        r += 1
        prod = re.search(str(sheet[r][1].value), 'Диван HOME')
        name = sheet[r][2].value
        if sheet[r][4].value:
            mod = str(sheet[r][3].value) + str(sheet[r][4].value)
        else:
            mod = str(sheet[r][3].value)
            
        price = str(sheet[r][6].value)

        if prod and name:
            if check_name != name:
                check_name = name
                prod_id += 1
                prom = sheet[r][0].value
                
                #print(Myakimebli.objects.filter(pars_name = name, manufacturer_id=5).update(pars_name = prom))
                
                print(prod_id, ':', prom, '-->', name)

                cards.append({
                    'id': prod_id,
                    'prom':prom,
                    'name': name,
                    'des':''
                })
        
            print(' ', prod_id, '-->', mod, price)

            size_cards.append({
                'id': prod_id,
                'name': mod,
                'w': 0,
                'h': 0,
                'd': 0,
                'w_s':0,
                'd_s':0,
                'price': num_check(price)
            })


    #Додаємо записи в базу
    for product in cards:
        print('------------------------------------------------')
        product['name']
        try:
            #Оновлюємо ціну
            if Myakimebli.objects.filter(pars_name = product['prom'], manufacturer_id=5):
                print('old', Myakimebli.objects.get(pars_name=product['prom']).myakimebli_name)
                model_id =  Myakimebli.objects.get(pars_name=product['prom']).id
                index = 0

                for s in size_cards:
                    if s['id'] == product['id']:
                        size_id = Product_myakimebli.objects.filter(myakimebli_name_id=model_id).values()[index]['id']
                        Product_myakimebli.objects.filter(id = size_id).update(price=s['price'])
                        index += 1
                
            #Додаємо новий товар
            else:
                new_id = Myakimebli.objects.all().order_by('-id')[0].id + 1

                Myakimebli.objects.get_or_create(id=new_id, manufacturer_id=5, myakimebli_name=product['name'],\
                    pars_name=product['prom'], description=product['des'])
                
                for s in size_cards:
                    if s['id'] == product['id']:
                        Product_myakimebli.objects.get_or_create(myakimebli_name_id=new_id,\
                             width=s['w'], height=s['h'], depth=s['d'],\
                                sleep_width=s['w_s'], sleep_depth=s['d_s'], price=s['price'])


                print('new', new_id, product['name'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')


def get_myakimebli_mixmebli():
    img_cards = []
    cards = []
    size_cards = []
    url = 'https://baustoff.com.ua/data/yml_mixmebli.xml'
    response = requests.get(url)
    categoryId = ['103',]


    print('response ', response.status_code)

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        for offer in root.find('.//shop/offers').iter('offer'):
            if offer.find('categoryId').text in categoryId and offer.attrib.get('available') == 'true':
                offer_id = offer.get('id')
                print(f"Offer ID: {offer_id}")

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
                    img_name = img.split('/')[len(img.split('/')) - 1]
                    img_bytes = requests.get(img).content
                    with open("/home/ay507291/notacomforta.pl.ua/www/media/" + img_name, "wb") as f:
                        f.write(img_bytes)

                    img_cards.append({
                        'id': offer_id,
                        'img': img_name
                    })
                
                print('------------------------------------')

    #Додаємо записи в базу
    new_db=[]
    for product in cards:
        print('------------------------------------------------')
        product['name']
        try:
            #Оновлюємо ціну
            if Myakimebli.objects.filter(pars_name = product['prom']):
                print('old', product['name'])
                model_id =  Myakimebli.objects.get(pars_name=product['prom']).id
                Myakimebli.objects.filter(id = model_id).update(sale = product['sale'])
                size_id = Product_myakimebli.objects.filter(myakimebli_name_id=model_id).values()[0]['id']
                new_db.append(product['name'])

                for s in size_cards:
                    if s['id'] == product['id']:
                        Product_myakimebli.objects.filter(id = size_id).update(price=s['price'])
                        break
                
            #Додаємо новий товар
            else:
                new_id = Myakimebli.objects.all().order_by('-id')[0].id + 1
                new_db.append(product['prom'])
                Myakimebli.objects.get_or_create(id=new_id, manufacturer_id=27,\
                                                 myakimebli_name=product['name'],\
                                                    pars_name=product['prom'], description=product['des'])
                
                for s in size_cards:
                    if s['id'] == product['id']:
                        Product_myakimebli.objects.get_or_create(myakimebli_name_id=new_id,\
                             width=s['w'], height=s['h'], depth=s['d'],\
                                sleep_width=s['w_s'], sleep_depth=s['d_s'], price=s['price'])

                for i in img_cards:
                    if i['id'] == product['id']:
                        Myakimebli_img.objects.get_or_create(myakimebli_img_id=new_id, img=i['img'])


                print('new', new_id, product['name'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')

    #Видаляємо товар
    for m in Myakimebli.objects.filter(manufacturer_id=27):
        if m.pars_name not in new_db:
            print('delet:', m)
            m.delete()