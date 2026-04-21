import requests
import xml.etree.ElementTree as ET
import json
from dribnytsi.models import Dribnytsi, Dribnytsi_size, Dribnytsi_img


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


def get_dribnytsi_mixmebli():

    img_cards = []
    cards = []
    size_cards = []
    url = 'https://baustoff.com.ua/data/yml_mixmebli.xml'
    response = requests.get(url)
    categoryId = ['90', '104']


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
            if Dribnytsi.objects.filter(pars_name = product['prom']):
                print('old', Dribnytsi.objects.get(pars_name=product['prom']).name)
                model_id =  Dribnytsi.objects.get(pars_name=product['prom']).id
                size_id = Dribnytsi_size.objects.filter(dribnytsi_id=model_id).values()[0]['id']
                new_db.append(product['prom'])
                for s in size_cards:
                    if s['id'] == product['id']:
                        Dribnytsi_size.objects.filter(id = size_id).update(price=s['price'])
                
            #Додаємо новий товар
            else:
                new_id = Dribnytsi.objects.all().order_by('-id')[0].id + 1
                new_db.append(product['prom'])
                Dribnytsi.objects.get_or_create(id=new_id, manufacturer_id=27, name=product['name'],\
                    pars_name=product['prom'], description=product['des'])
                
                for s in size_cards:
                    if s['id'] == product['id']:
                        Dribnytsi_size.objects.get_or_create(dribnytsi_id=new_id,\
                            w=s['w'], d=s['d'], price=s['price'])

                for i in img_cards:
                    if i['id'] == product['id']:
                        Dribnytsi_img.objects.get_or_create(key_img_id=new_id, img=i['img'])


                print('new', new_id, product['name'])

        except Exception as ex:
            print('///----------ERORR--------///')
            print(ex)
            print('///----------ERORR--------///')