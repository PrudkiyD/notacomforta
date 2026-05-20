from catalog.models import Product
from googletrans import Translator


#ff


HEADERS = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}

product_images_path = "/home/ay507291/notacomforta.pl.ua/www/media/"
file_path = "/home/ay507291/notacomforta.pl.ua/www"


def num_check(text):
    num = ''
    for t in str(text):
        if t.isdigit():
            num += t
    return num

def change_category(manufacturer, old_category, external_id, external_category):
  
    product = Product.objects.filter(
        external_id=external_id,
        manufacturer_id=manufacturer,
        external_category=old_category
    )

    if product.exists():
        product = product.first()
        product.external_category = external_category
        product.save()


def change_category_modul(manufacturer, old_category, external_id, external_category, seria):
  
    product = Product.objects.filter(
        external_id=external_id,
        manufacturer_id=manufacturer,
        external_category=old_category,
        seria=seria
    )

    if product.exists():
        product = product.first()
        product.external_category = external_category
        product.save()



def trans(text):
    translator = Translator().translate(text=text, src='ru', dest='uk')
    return translator.text

