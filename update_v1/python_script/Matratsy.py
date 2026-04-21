import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from googletrans import Translator
from matrasy.models import Matrasy, Matrasy_img, Matrasy_size
import json
import re


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
    for t in text:
        if t.isdigit():
            num += t
    return num


def trans(text):
    translator = Translator().translate(text=text, src='ru', dest='uk')
    return translator.text

def Up():
    c_list = []
    for i in Matrasy.objects.all():
        if i.name not in c_list:
            c_list.append(i.name)
        else:
            print(i.name)

def get_matrasy_matrolux():
    print('Start ...')
    req = requests.get('https://matroluxe.ua/index.php?route=extension/feed/yandex_yml9',headers=HEADERS)  
    src = req.text
    print(src[:500])

    soup = BeautifulSoup(src, 'xml')
    item = soup.find_all('offer')

    cards = []
    size_cards = []
    img_cards = []
    offer_list = []
    prod_id = ''

    for i in item:
        name_list = str(i.find('name').get_text()).split(',')
        desc_text = '<p>' + str(i.find('description').get_text()) + '</p>'
        offer_id = i.get('group_id')
        prom = i.get('id')
        

        if offer_id not in offer_list and offer_id:
            offer_list.append(offer_id)
            picture = i.find_all('picture')
            img_list = []
            print(len(offer_list), '-->', name_list[0], '-->', prom)

            for i in picture:
                img_list.append(i.get_text())

            for i in img_list:
                img_name = i
                img_cards.append({
                    'id': offer_id,
                    'img': img_name
            })

            cards.append({
                'id': offer_id,
                'prom':prom,
                'name': name_list[0],
                'des': desc_text,
            })

            

    for i in item:
        price = i.find('price').get_text()
        size = ['', '', '']
        param_list = i.find_all('param')
        param = ''
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

            param += (
                f"<tbody>"\
                    f"<tr>"\
                        f"<td>{p.get('name')}</td>"\
                        f"<td>{p.get_text()}</td>"\
                    f"</tr>"\
                f"</tbody>"
            )


        size_cards.append({
                'id': offer_id,
                'option': option,
                'param': param,
                'w': size[0],
                'h': '',
                'd': size[1],
                'price': price,
        })

    #Додаємо записи в базу
    new_db=[]
    for product in cards:
        print('------------------------------------------------')

        try:
            #Оновлюємо ціну
            if Matrasy.objects.filter(pars_name = product['prom']).filter(manufacturer_id=23):

                

                print('old', Matrasy.objects.get(pars_name=product['prom']).name)
                model_id =  Matrasy.objects.get(pars_name=product['prom']).id
                new_db.append(product['prom'])
                index = 0

                for s in size_cards:
                    if s['id'] == product['id']:
                        size_id = Matrasy_size.objects.filter(matrasy_id=model_id).values()[index]['id']
                        Matrasy_size.objects.filter(id = size_id).update(price=s['price'])
                        index += 1
                
            #Додаємо новий товар
            else:
                new_id = Matrasy.objects.all().order_by('-id')[0].id + 1
                new_db.append(product['prom'])
                Matrasy.objects.get_or_create(id=new_id, manufacturer_id=23, name=product['name'],\
                    pars_name=product['prom'], description=product['des'])
                
                for s in size_cards:
                    if s['id'] == product['id']:
                        Matrasy_size.objects.get_or_create(matrasy_id=new_id, option=s['option'],\
                            param=s['param'], w=s['w'], h=s['h'], d=s['d'], price=s['price'])

                for i in img_cards:
                    if i['id'] == product['id']:
                        Matrasy_img.objects.get_or_create(key_img_id=new_id, img=i['img'])

                print('new', new_id, product['name'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')
    '''
    #Видаляємо товар
    for m in Matrasy.objects.filter(manufacturer_id=23):
        if m.pars_name not in new_db:
            print('delet:', m)
            m.delete()
    '''

def get_matrasy_emm():
    print('Start...')

    src = requests.get('https://emm.ua/prom.xml',headers=HEADERS).text
    print('Get src ---///')

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
                img_name = i
                img_cards.append({
                    'id': offer_id,
                    'img': img_name
            })
            

            cards.append({
                'id': offer_id,
                'prom': prom,
                'name': name_list[0],
                'des': desc_text,
            })


    for i in item:
        price = i.find('price').get_text()[:-3]
        size_list = name_list = str(i.find('name').get_text()).split('-')[1]
        size = size_list.split('х')
        param_list = i.find_all('param')
        param = ''
        offer_id = i.get('group_id')
        option = ''

        for p in param_list:

            if p.get('name') == 'Тип пружинного блока':
                option = p.get_text()

            param += (
                f"<tbody>"\
                    f"<tr>"\
                        f"<td>{p.get('name')}</td>"\
                        f"<td>{p.get_text()}</td>"\
                    f"</tr>"\
                f"</tbody>"
            )

        try:
            size = size_list.split('х')

            size_cards.append({
                'id': offer_id,
                'option': option,
                'param': param,
                'w': size[0],
                'h': '',
                'd': size[1],
                'price': price,
            })
        except:
            size_cards.append({
                'id': offer_id,
                'option': option,
                'param': param,
                'w': '',
                'h': '',
                'd': '',
                'price': price,
            })

        print(offer_id, '-->', option, size, price)


    #Додаємо записи в базу
    new_db=[]
    for product in cards:
        print('------------------------------------------------')
        product['name']
        try:
            #Оновлюємо ціну
            if Matrasy.objects.filter(pars_name = product['prom']):
                print('old', Matrasy.objects.get(pars_name=product['prom']).name)
                model_id =  Matrasy.objects.get(pars_name=product['prom']).id
                new_db.append(product['prom'])
                index = 0

                for s in size_cards:
                    if s['id'] == product['id']:
                        size_id = Matrasy_size.objects.filter(matrasy_id=model_id).values()[index]['id']
                        Matrasy_size.objects.filter(id = size_id).update(price=s['price'])
                        index += 1
                
            #Додаємо новий товар
            else:
                new_id = Matrasy.objects.all().order_by('-id')[0].id + 1
                new_db.append(product['prom'])
                Matrasy.objects.get_or_create(id=new_id, manufacturer_id=15, name=product['name'],\
                    pars_name=product['prom'], description=product['des'])
                
                for s in size_cards:
                    if s['id'] == product['id']:
                        Matrasy_size.objects.get_or_create(matrasy_id=new_id, option=s['option'],\
                            param=s['param'], w=s['w'], h=s['h'], d=s['d'], price=s['price'])

                for i in img_cards:
                    if i['id'] == product['id']:
                        Matrasy_img.objects.get_or_create(key_img_id=new_id, img=i['img'])

                print('new', new_id, product['name'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')

    #Видаляємо товар
    for m in Matrasy.objects.filter(manufacturer_id=15):
        if m.pars_name not in new_db:
            print('delet:', m)
            m.delete()

def get_matrasy_eurosleep():
    cards = []
    img_cards = []
    size_cards = []
    prod_link = []

    # Забераємо пагенацію

    src = requests.get('https://eurosleep.ua/uk/toppery-i-tonkie-matrasy/', headers=HEADERS)
    soup = BeautifulSoup(src.content, 'lxml')
    pag_list = ['https://eurosleep.ua/uk/toppery-i-tonkie-matrasy/', 'https://eurosleep.ua/uk/ortopedicheskie-matrasy/']
    pagination = soup.find('ul', class_='pagination').find_all('a')

    for p in pagination:
        pag = p.get('href')
        if pag not in pag_list:
            print(pag)
            pag_list.append(pag)


    src = requests.get('https://eurosleep.ua/uk/ortopedicheskie-matrasy/', headers=HEADERS)
    soup = BeautifulSoup(src.content, 'lxml')
    pagination = soup.find('ul', class_='pagination').find_all('a')

    for p in pagination:
        pag = p.get('href')
        if pag not in pag_list:
            print(pag)
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
                print(len(prod_link) - 1, ':', link)

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

        print(url['num'], name)

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
                        'option': '',
                        'param': '',
                        'w': size[0],
                        'h': '',
                        'd': size[1],
                        'price': price,
                    })

                except:
                    pass

                print(url['num'], size, price)
        
        for i in img_list:
            img_name = i.get('href')

            img_cards.append({
                'id': url['num'],
                'img': img_name
            })
            print(img_name)

        print('----------------------------------------------------')
        time.sleep(1)

    #Додаємо записи в базу
    new_db = []
    for product in cards:
        print('------------------------------------------------')
        product['name']
        try:
            #Оновлюємо ціну
            if Matrasy.objects.filter(pars_name = product['prom']):
                print('old', Matrasy.objects.get(pars_name=product['prom']).name)
                model_id =  Matrasy.objects.get(pars_name=product['prom']).id
                new_db.append(product['prom'])
                index = 0

                for s in size_cards:
                    if s['id'] == product['id']:
                        size_id = Matrasy_size.objects.filter(matrasy_id=model_id).values()[index]['id']
                        Matrasy_size.objects.filter(id = size_id).update(price=s['price'],)
                        index += 1
                
            #Додаємо новий товар
            else:
                new_id = Matrasy.objects.all().order_by('-id')[0].id + 1
                new_db.append(product['prom'])
                Matrasy.objects.get_or_create(id=new_id, manufacturer_id=16, name=product['name'],\
                    pars_name=product['prom'], description=product['des'])
                
                for s in size_cards:
                    if s['id'] == product['id']:
                        Matrasy_size.objects.get_or_create(matrasy_id=new_id, option=s['option'],\
                            param=s['param'], w=s['w'], h=s['h'], d=s['d'], price=s['price'])

                for i in img_cards:
                    if i['id'] == product['id']:
                        Matrasy_img.objects.get_or_create(key_img_id=new_id, img=i['img'])

                print('new', new_id, product['name'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')

    #Видаляємо товар
    for m in Matrasy.objects.filter(manufacturer_id=16):
        if m.pars_name not in new_db:
            print('delet:', m)
            m.delete()
