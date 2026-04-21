import requests
import openpyxl
import re
from main.models import Stinka, Stinka_img
from pars.models import File

def get_other_neman():
    path ="/home/ay507291/notacomforta.pl.ua/www"+File.objects.get(id=9).file_up.url
    print(path)
    book = openpyxl.load_workbook(filename=path)
    sheet_1 = book.worksheets[0]

    prod_id = 0
    cards = []
    img_cards = []

    for r in range(sheet_1.max_row):
        r += 1

        cell = str(sheet_1[r][3].value)
        match = re.search('Дзеркало', cell)
        match2 = re.search('Полиця', cell)

        if match or match2:
            prod_id += 1
            prom = str(sheet_1[r][0].value)
            name = str(sheet_1[r][5].value)
            des = str(sheet_1[r][37].value)
            name_ru = str(sheet_1[r][6].value)
            des_ru = str(sheet_1[r][38].value)
            price = str(sheet_1[r][9].value)[:-3]
            img_list = str(sheet_1[r][15].value).split(';')
            img_list = [line.rstrip() for line in img_list]

            cards.append({
                'id': prod_id,
                'prom':prom,
                'name': name,
                'name_ru': name_ru,
                'des': des,
                'des_ru': des_ru,
                'w': '',
                'h': '',
                'd': '',
                'price': price,
            })



            for i in img_list:
                try:
                    img = i
                    img_name = img.split('/')[len(img.split('/')) - 1]
                    img_name = str(img_name).replace('%', '')
                    img_bytes = requests.get(img).content
                    with open("/home/ay507291/notacomforta.pl.ua/www/media/" + img_name, "wb") as f:
                        f.write(img_bytes)

                    img_cards.append({
                        'id': prod_id,
                        'img': img_name
                    })
                except:
                    pass

            print('--------------------------')
            print(prom)
            print(name, price)

    #Додаємо записи в базу
    for product in cards:
        print('------------------------------------------------')
        product['name']
        try:
            #Оновлюємо ціну
            if Stinka.objects.filter(pars_name = product['prom']).filter(manufacturer_id=10):
                print('old', Stinka.objects.get(pars_name=product['prom']).name)
                model_id =  Stinka.objects.get(pars_name=product['prom']).id
                Stinka.objects.filter(id = model_id).update(price=product['price'])
                        
                
            #Додаємо новий товар
            else:
                new_id = Stinka.objects.all().order_by('-id')[0].id + 1

                Stinka.objects.get_or_create(id=new_id, manufacturer_id=10,\
                    name=product['name'], name_ru = product['name_ru'],\
                        description=product['des'], description_ru=product['des_ru'], pars_name=product['prom'],\
                            categori = "OTHER", price=product['price'])

                for i in img_cards:
                    if i['id'] == product['id']:
                        Stinka_img.objects.get_or_create(key_img_id=new_id, img=i['img'])

                print('new', new_id, product['name'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')