from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Cart, CartOrderItem, Order
from catalog.models import Product, ProductPrice, ProductImage
import uuid
from django.utils import timezone
from page.models import Page, Element
from catalog.models import Category
from django.shortcuts import redirect
import random
import requests
import os


def get_cart(cart):
    # Отримуємо всі елементи в кошику
    cart_items = CartOrderItem.objects.filter(cart=cart)

    # Список товарів у кошику
    items_list = []
    total_sum = 0

    for item in cart_items:
        item_total_price = item.quantity * float(item.product_price.price)
        total_sum += item_total_price

        items_list.append({
            "img":item.img,
            "product_id": item.product.id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price_per_unit": float(item.product_price.price),
            "price_id": float(item.product_price.id),
            "total_price": item_total_price,
            "coment": item.coment,
        })

    # Формуємо JSON-відповідь
    response_data = {
        "cart_id": cart.id,
        "customer_key": cart.customer_key,
        "created_at": cart.created_at.isoformat(),
        "total_sum": total_sum,
        "items": items_list
    }

    return response_data


def item_product(customer_key, product_id, price_id, add=True, quantity=0):
    try:
        
        # Отримуємо кошик
        cart = Cart.objects.get(customer_key=customer_key)

        # Отримуємо продукт і ціну
        product = Product.objects.get(id=product_id)
        price = ProductPrice.objects.get(id=price_id)

        # Додаємо або отримуємо елемент кошика

        try:
            main_img = str(ProductImage.objects.filter(product_id=product, is_main=True).first().image.name)

            if main_img[0:4] == 'http':
                pass

            else:
                main_img = str(ProductImage.objects.filter(product_id=product, is_main=True).first().image.url)

            item, created = CartOrderItem.objects.get_or_create(
                cart=cart,
                product=product,
                product_price=price,
                defaults={"quantity": 1, "img":main_img}
            )
        
        except:
            item, created = CartOrderItem.objects.get_or_create(
                cart=cart,
                product=product,
                product_price=price,
                defaults={"quantity": 1, "img":"/media/undefined.svg"}
            )

        if not created:
            if add:
                item.quantity += 1
                item.save()
            else:
                if item.quantity - 1 <= 0:
                    item.delete()

                else:
                    item.quantity -= 1
                    item.save()

            if add and quantity:
                if item.quantity - 1 <= 0 or int(quantity) <= 0:
                    item.delete()

                else:
                    item.quantity = int(quantity)
                    item.save()

        return JsonResponse(get_cart(cart))
    except Cart.DoesNotExist:
        return JsonResponse({"error": "Cart not found."}, status=404)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found."}, status=404)
    except ProductPrice.DoesNotExist:
        return JsonResponse({"error": "Price not found."}, status=404)



def index(request):
    return render(request, 'index.html')


def cart(request, customer_key):
    # Отримуємо кошик за customer_key або 404
    cart = get_object_or_404(Cart, customer_key=customer_key)
    return JsonResponse(get_cart(cart))


def createkey(request):
    # Генеруємо унікальний ключ
    unique_key = str(uuid.uuid4())
    
    # Створюємо новий об'єкт Cart
    cart = Cart.objects.create(
        customer_key=unique_key,
        created_at=timezone.now()
    )

    # Відповідь у форматі JSON
    return JsonResponse({
        "cart_key": cart.customer_key,
    })


def add_to_cart(request, customer_key, product_id, price_id):
    return item_product(customer_key, product_id, price_id, add=True)
    

def minus(request, customer_key, product_id, price_id):
    return item_product(customer_key, product_id, price_id, add=False)


def quantity(request, customer_key, product_id, price_id, quantity):
    return item_product(customer_key, product_id, price_id, add=True, quantity=quantity)


def generate_unique_order_id():
    while True:
        order_id = str(random.randint(1000000, 9999999))  # Генеруємо 7-значне число
        if not Order.objects.filter(id=order_id).exists():
            return order_id

def successful(request):
    try:
        if request.method == 'POST':
            # Отримання даних із форми
            key = request.POST.get('key', '')
            customer = request.POST.get('customer', '')
            phone = request.POST.get('phone', '')
            coment = request.POST.get('coment', '')

            # Отримання кошика за `customer_key`
            cart = get_object_or_404(Cart, customer_key=key)

            order_id = generate_unique_order_id()

            while True:
                if Order.objects.filter(id=order_id).exists():
                    order_id = generate_unique_order_id()
                
                else:
                    break

            # Створення замовлення
            order = Order.objects.create(
                id=order_id,
                customer=customer,
                phone=phone,
                coment=coment,
                total=sum(item.product_price.price * item.quantity for item in cart.items.all()),
            )

            # Переміщення товарів із кошика до замовлення
            for item in cart.items.all():
                item.order = order  # Прив'язуємо до замовлення
                item.cart = None    # Видаляємо прив'язку до кошика
                item.save()

            # Видалення кошика
            cart.delete()

            try:
                admins = os.getenv('TG_ID_ADMIN').split(',')

                text_ms = (f"📦 <b>Номер замовлення:</b> {order.id}\n"
                        f"👤 <b>Прізвище та ім'я:</b> {order.customer}\n"
                        f"📞 <b>Телефон:</b> {order.phone}\n"
                        f"💬 <b>Коментар:</b> {order.coment}\n"
                        f"💰 <b>Сума:</b> {order.total} грн")

                for chat_id in admins:

                    requests.post(
                        f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage",
                        json={
                            'chat_id': chat_id.strip(),
                            'text': text_ms,
                            'parse_mode': 'HTML',
                            'reply_markup': {
                                'inline_keyboard': [
                                    [
                                        {
                                            'text': '🔎 Переглянути на сайті',
                                            'url': f'https://www.notacomforta.pl.ua/order/track?number={order.id}'
                                        }
                                    ],
                                    [
                                        {
                                            'text': '🔧 Адмін панель',
                                            'url': f'https://www.notacomforta.pl.ua/admin/order/order/{order.id}/change/'
                                        }
                                    ]
                                ]
                            }
                        }
                    )
                    
            except Exception as ex:
                text_ms = f"💬 <b>Сталася помилка при відправленні повідомлення:</b> {ex}"
                for chat_id in admins:
                    requests.post(
                            f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage",
                            json={
                                'chat_id': chat_id.strip(),
                                'text': text_ms,
                                'parse_mode': 'HTML',
                            }
                        )

            return redirect(f'/order/successful/{order.id}')
    except Exception as ex:
        print(ex)
        return redirect('/')
    

def successful_track(request, order_id):
    categorys = Category.objects.prefetch_related('subcategories')
    pages = Page.objects.filter(published=True)
    order = Order.objects.get(id=order_id)

    return render(request, 'successful.html', {
        'title': "Успішно оформлене замовлення",
        'order': order,
        'pages':pages,
        'categorys': categorys,
    })


def track(request):
    categorys = Category.objects.prefetch_related('subcategories')
    pages = Page.objects.filter(published=True)

    order_id = request.GET.get('number')
    order = []

    
    if order_id:
        order = get_object_or_404(Order, id=order_id)

    return render(request, 'order-track.html', {
        'title': "Відстежити замовлення",
        'order': order,
        'pages':pages,
        'categorys': categorys,
    })