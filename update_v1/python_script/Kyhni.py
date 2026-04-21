import requests
from bs4 import BeautifulSoup
import csv
import time
import json
import xml.etree.ElementTree as ET
from kyhni.models import Kyhni, Kyhni_img
import openpyxl
from pars.models import File


with open('/home/ay507291/notacomforta.pl.ua/www/pars/src.json', 'r') as f:
    file = json.load(f)

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


def get_seria_komfortmebli():
    path ="/home/ay507291/notacomforta.pl.ua/www"+File.objects.get(id=17).file_up.url
    print(path)
    book = openpyxl.load_workbook(filename=path)
    sheet = book.worksheets[0]
    cards = []
    img_cards = []
    prod_id = 0

    for r in range(sheet.max_row):
        r += 1
        cell = str(sheet[r][1].value)

        if r != 1:

            prod_id += 1
            prom = str(sheet[r][0].value)
            name = str(sheet[r][1].value)
            price = str(sheet[r][2].value)
            imgs = f"{sheet[r][13].value};{sheet[r][15].value}"
            img_list = imgs.split(';')


            des = (
                        f"<tbody>\n"
                        f"    <tr>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>Форма кухні</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>{sheet[r][4].value}</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"    </tr>\n"
                        f"    <tr>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>Довжина кухні</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>{sheet[r][5].value}</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"    </tr>\n"
                        f"    <tr>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>Стиль</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>{sheet[r][6].value}</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"    </tr>\n"
                        f"    <tr>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>Відтінки фасаду</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>{sheet[r][7].value}</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"    </tr>\n"
                        f"    <tr>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>Покриття фасадів</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>{sheet[r][8].value}</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"    </tr>\n"
                        f"    <tr>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>Колір корпусу кухні</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>{sheet[r][9].value}</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"    </tr>\n"
                        f"    <tr>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>Серія</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>{sheet[r][10].value}</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"    </tr>\n"
                        f"    <tr>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>Колір фасаду кухні</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"        <td>\n"
                        f"            <p>\n"
                        f"                <span>{sheet[r][11].value}</span>\n"
                        f"            </p>\n"
                        f"        </td>\n"
                        f"    </tr>\n"
                        f"</tbody>\n"
                        f"<p>{sheet[r][16].value}</p>"
                    )


            cards.append({
                'prom':prom, 
                'id': prod_id,
                'name': name,
                'des': des,
                'price':price
            })

            print(prom, '-->', name, '->', price)

            for img in img_list:
                print(f"->{img} \n")
                try:
                    img_name = img.split('/')[len(img.split('/')) - 1]
                    img_bytes = requests.get(img).content
                    with open("/home/ay507291/notacomforta.pl.ua/www/media/" + img_name, "wb") as f:
                        f.write(img_bytes)

                    img_cards.append({
                        'id': prod_id,
                        'img': img_name
                    })

                except Exception as ex:
                    print(f'error->{ex} \n')

            
            print('-------------------------')

    
    #Додаємо записи в базу
    new_db=[]
    for product in cards:
        print('------------------------------------------------')
        try:
            #Оновлюємо ціну
            if Kyhni.objects.filter(pars_name = product['prom']):
                print('old', Kyhni.objects.get(pars_name=product['prom']).seria)
                model_id = Kyhni.objects.get(pars_name=product['prom']).id
                Kyhni.objects.filter(id = model_id).update(price=product['price'])

                new_db.append(product['prom'])

            #Додаємо новий товар
            else:
                new_id = Kyhni.objects.all().order_by('-id')[0].id + 1
                new_db.append(product['prom'])

                Kyhni.objects.get_or_create(id=new_id, manufacturer_id=1, seria=product['name'],\
                    pars_name=product['prom'], description=product['des'], price=product['price'])

                for i in img_cards:
                    if i['id'] == product['id']:
                        Kyhni_img.objects.get_or_create(seria_img_id=new_id, img=i['img'])


                print('new', new_id, product['name'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')
    
    
    #Видаляємо товар
    for m in Kyhni.objects.filter(manufacturer_id = 1):
        print(m)
        if m.pars_name not in new_db:
            print('delet:', m)
            m.delete()


def get_seri_svitmebliv():
    source = requests.get('https://www.svit-mebliv.ua/catalog/kuhni', headers=HEADERS).text
    soup = BeautifulSoup(source, 'html.parser')
    cards = []
    img_cards = []

    #Збираєм пагінацію
    items = soup.find_all('a', class_='pagination__link')
    pag_list = ['https://www.svit-mebliv.ua/catalog/kuhni',]
    for i in items:
        pag = 'https://www.svit-mebliv.ua'+str(i.get('href'))

        if pag not in pag_list:
            pag_list.append(pag)

    #Збираємо посилання на товар
    prod_list = []
    check_list =[]
    for p in pag_list:
        source = requests.get(p, headers=HEADERS).text
        soup = BeautifulSoup(source, 'html.parser')

        items = soup.find_all('div', class_='bedroom-sets-block-img')

        for i in items:
            link = 'https://www.svit-mebliv.ua'+str(i.find('a').get('href'))

            if link not in check_list:
                check_list.append(link)

                prod_list.append({
                    'id':len(check_list),
                    'link':link
                })

    #Збираємо інформацію про товар
    for p in prod_list:
        source = requests.get(p['link'], headers=HEADERS).text
        soup = BeautifulSoup(source, 'html.parser')

        name = soup.find('h1').getText()
        des = soup.find('div', class_='product-card-parameters')
        img_list = soup.find('div', class_='product-card-slider-bottom').find_all('div', class_='product-card-slider-bottom__img')

        print(f"///---{p['id']}------>{name}---///")

        cards.append({
            'id': p['id'],
            'name': name,
            'des': str(des),
            'price':''
        })

        for i in img_list:
            img = 'https://www.svit-mebliv.ua'+str(i.find('a').get('href'))
            img_name = img.split('/')[len(img.split('/')) - 1]
            img_bytes = requests.get(img, headers=HEADERS).content
            with open("/home/ay507291/notacomforta.pl.ua/www/media/" + img_name, "wb") as f:
                f.write(img_bytes)

            img_cards.append({
                'id': p['id'],
                'img': img_name
            })

            print(f"{p['id']}---{img}")
        time.sleep(1)

    #Додаємо записи в базу
    for product in cards:
        print('------------------------------------------------')
        try:
        #Оновлюємо ціну
            if Kyhni.objects.filter(pars_name = product['name']):
                print('old', Kyhni.objects.get(pars_name=product['name']).seria)

            #Додаємо новий товар
            else:
                new_id = Kyhni.objects.all().order_by('-id')[0].id + 1
                print('1')
                Kyhni.objects.get_or_create(id=new_id, manufacturer_id=2, seria=product['name'],\
                    pars_name=product['name'], description=product['des'], price=product['price'])
                print('2')
                for i in img_cards:
                    if i['id'] == product['id']:
                        Kyhni_img.objects.get_or_create(seria_img_id=new_id, img=i['img'])

                print('new', new_id, product['name'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')
        
