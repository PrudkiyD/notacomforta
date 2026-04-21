import requests
import json
import xml.etree.ElementTree as ET

with open('/home/ay507291/notacomforta.pl.ua/www/pars/src.json', 'r') as f:
    file = json.load(f)

accept = file['src'][1]['accept']
user_agent = file['src'][2]['user-agent']

HEADERS = {
    'accept': accept,
    'user-agent': user_agent
}

def dev():
    print('Start ...')
    req = requests.get('https://matroluxe.ua/index.php?route=extension/feed/yandex_yml5', headers=HEADERS)
    src = req.text
    print('Get src ---///')

    # Парсинг XML
    root = ET.fromstring(src)
    
    # Отримаємо список товарів
    offers = root.findall('.//offer')

    for offer in offers:
        # Виведення всіх полів
        product_id = offer.get('id')
        available = offer.get('available')
        group_id = offer.get('group_id')
        url = offer.find('url').text if offer.find('url') is not None else 'Немає URL'
        price = offer.find('price').text if offer.find('price') is not None else 'Немає ціни'
        currency_id = offer.find('currencyId').text if offer.find('currencyId') is not None else 'Немає валюти'
        category_id = offer.find('categoryId').text if offer.find('categoryId') is not None else 'Немає категорії'
        
        # Виведення picture як список
        pictures = offer.findall('picture')
        picture_list = [pic.text for pic in pictures]
        
        store = offer.find('store').text if offer.find('store') is not None else 'Немає інформації про магазин'
        pickup = offer.find('pickup').text if offer.find('pickup') is not None else 'Немає інформації про самовивіз'
        delivery = offer.find('delivery').text if offer.find('delivery') is not None else 'Немає інформації про доставку'
        stock_quantity = offer.find('stock_quantity').text if offer.find('stock_quantity') is not None else 'Немає кількості на складі'
        name = offer.find('name').text if offer.find('name') is not None else 'Немає назви'
        vendor = offer.find('vendor').text if offer.find('vendor') is not None else 'Немає постачальника'
        manufacturer_warranty = offer.find('manufacturer_warranty').text if offer.find('manufacturer_warranty') is not None else 'Немає гарантії'

        # Виведення параметрів
        params = offer.findall('param')
        param_dict = {param.get('name'): param.text for param in params}

        # Виведення даних
        print(f'ID: {product_id}')
        print(f'Available: {available}')
        print(f'Group ID: {group_id}')
        print(f'URL: {url}')
        print(f'Price: {price}')
        print(f'Currency ID: {currency_id}')
        print(f'Category ID: {category_id}')
        print(f'Pictures: {picture_list}')
        print(f'Store: {store}')
        print(f'Pickup: {pickup}')
        print(f'Delivery: {delivery}')
        print(f'Stock Quantity: {stock_quantity}')
        print(f'Name: {name}')
        print(f'Vendor: {vendor}')
        print(f'Manufacturer Warranty: {manufacturer_warranty}')
        print(f'Parameters: {param_dict}')
        print('-' * 50)
