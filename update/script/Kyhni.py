from catalog.models import Product, ProductImage, ProductPrice, Category
from .Tools import HEADERS, change_category, change_category_modul, file_path, product_images_path, num_check
from update.models import File, History
from bs4 import BeautifulSoup
import requests
import time
import openpyxl


def get_seria_komfortmebli():
    path = File.objects.get(id=1).files
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
                    img_cards.append({
                        'id': prod_id,
                        'img': img_name,
                        'url': img
                    })

                except Exception as ex:
                    print(f'error->{ex} \n')

            
            print('-------------------------')
    

    #Додаємо записи в базу

    stock = []

    for item in cards:
        category = Category.objects.get(id=2)
        manufacturer = 1
        external_category = 'get_seria_komfortmebli'

        change_category(manufacturer, 'kyhni', item['prom'], external_category)

        try:
        #Оновлюємо ціну
            product = Product.objects.filter(
                external_id=item['prom'],
                manufacturer_id=manufacturer,
                external_category=external_category
            )

            if product.exists():
                price = ProductPrice.objects.filter(product=product.first()).first()

                price.price = item['price']
                price.save()

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

                prace_product = ProductPrice.objects.create(
                            product=product,
                            price=item['price'],
                            is_main=True,
                        )
                
                prace_product.save()

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



def get_seri_svitmebliv():
    print('Кухні ...')
    src_url = File.objects.get(id=2).url
    source = requests.get(src_url, headers=HEADERS).text
    soup = BeautifulSoup(source, 'html.parser')
    cards = []
    img_cards = []

    #Збираєм пагінацію
    items = soup.find_all('a', class_='pagination__link')
    pag_list = [src_url,]
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

        cards.append({
            'id': p['id'],
            'name': name,
            'prom':name,
            'des': str(des),
            'price':0
        })

        for i in img_list:
            img = 'https://www.svit-mebliv.ua'+str(i.find('a').get('href'))
            img_name = img.split('/')[len(img.split('/')) - 1]

            img_cards.append({
                'id': p['id'],
                'img': img_name,
                'url': img
            })

        time.sleep(1)

    #Додаємо записи в базу

    stock = []
    external_category = 'get_seri_svitmebliv'

    for item in cards:
        category = Category.objects.get(id=2)
        manufacturer = 2
        

        change_category(manufacturer, 'kyhni', item['prom'], external_category)

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

                prace_product = ProductPrice.objects.create(
                            product=product,
                            price=item['price'],
                            is_main=True,
                        )
                
                prace_product.save()

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