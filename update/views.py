from django.shortcuts import render
from django.shortcuts import redirect
from catalog.models import ProductPrice
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseForbidden
import json
from .tasks import update_task

from .script import Kyhni, Shafi, Myakimebli, Lizhka, \
                    Matratsy, Komody_tumby, Peredpokoi, Vitalni, Spalni, \
                    Dytyachi, Matrolux_module, Stoly, Pcstoly, \
                    Kukhonni_kutochky, Stiltsi_taburety, RichmanUpdate

def update(request):
    msg = False

    

    if not request.user.is_superuser:
        return redirect('/admin')

    if request.GET.get('manufacturer'):
        try:
            manufacturer = request.GET.get('manufacturer')

            try:
                manufacturer = int(manufacturer)
            except:
                pass

            if manufacturer == 0:
                msg = 'Оберіть виробника'
            
            else:
                update_task.delay(manufacturer)
                msg = '<div class="msg">Оновлення розпочалося.</div> <br> <a class="msg-url" href="/admin/update/taskexecution/">Переглянути</a>'

            
        except Exception as ex:
            msg = f"Сталася помилка при оновленні."
            print(ex)
  
    return render(request, 'update.html', {'msg': msg,})



@require_POST
def discount(request):
    # Перевірка на суперкористувача
    if not request.user.is_superuser:
        return JsonResponse({"error": "Access denied"}, status=400)
    

    try:
        data = json.loads(request.body)

        discount_value = data.get('discount')
        product_list = data.get('product')

        if product_list[0] == 'on':
            product_list = product_list[1:]

        prices = ProductPrice.objects.filter(product__in=product_list)


        if discount_value:
            for p in prices:
                price = p.price
                d = round((price / 100) * int(discount_value[1:]))

                if discount_value[0] == '+':
                    p.price = price + d
                    p.save()

                if discount_value[0] == '-':
                    p.price = price - d
                    p.save()

        # Тепер можна працювати з даними з JSON
        return JsonResponse({"status": "ok", "received": data}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
