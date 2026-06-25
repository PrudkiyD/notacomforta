from django.shortcuts import render
from django.shortcuts import redirect
from catalog.models import ProductPrice
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseForbidden
import json

from .script import Kyhni, Shafi, Myakimebli, Lizhka, \
                    Matratsy, Komody_tumby, Peredpokoi, Vitalni, Spalni, \
                    Dytyachi, Matrolux_module, Stoly, Pcstoly, \
                    Kukhonni_kutochky, Stiltsi_taburety

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
            

            if manufacturer == 1:
                Kyhni.get_seria_komfortmebli()
                Shafi.get_prod_komfortmebli()
                Lizhka.get_lizhka_komfortmebli()
                Vitalni.get_vitalni_products_comfortmebli()
                Spalni.get_spalni_products_comfortmebli()
                Peredpokoi.get_peredpokoi_products_comfortmebli()
                Dytyachi.get_dytyachi_products_comfortmebli()
                Komody_tumby.get_komody_tumby_comfortmebli()
                Pcstoly.get_pcstoly_comfortmebli()

                 
                
                

            if manufacturer == 2:
                Kyhni.get_seri_svitmebliv()
                '''Shafi.get_shafi_svitmebliv()
                Shafi.get_stelazhi_svitmebliv()
                Lizhka.get_lizhka_product_svitmebliv()
                Vitalni.get_vitalni_products_svitmebliv()
                Peredpokoi.get_peredpokoi_products_svitmebliv()
                Spalni.get_spalni_products_svitmebliv()
                Dytyachi.get_dytyachi_products_svitmebliv()
                Komody_tumby.get_komody_tumby_svitmebliv()'''

                 


            if manufacturer == 3:
                pass


            if manufacturer == 4:
                Shafi.get_link_matrolux()
                Myakimebli.get_myaki_mebli_matrolux()
                Lizhka.get_lizhka_products_matrolux()
                Matrolux_module.get_stinka_matrolux()
                Matratsy.get_matrasy_matrolux()
                Komody_tumby.get_komody_tumby_matrolux()
                Stoly.get_stoly_matrolux()
                Pcstoly.get_pcstoly_matrolux()

                 
            if manufacturer == 5:
                Shafi.get_products_fenix()

                 


            if manufacturer == 6:
                Myakimebli.get_products_richman()
                Lizhka.get_lizhka_product_richman()

                 


            if manufacturer == 7:
                Lizhka.get_lizhka_product_lion() #Немає файла для оновлення
                Komody_tumby.get_komody_tumby_lion()

                 


            if manufacturer == 8:
                Vitalni.get_vitalni_products_bmk()

                 


            if manufacturer == 9:
                Vitalni.get_vitalni_products_gerbor()
                Peredpokoi.get_peredpokoi_products_gerbor()

                 

            
            if manufacturer == 10:
                Lizhka.get_lizhka_product_everest()
                Komody_tumby.get_komody_tumby_everest()

                 

            
            if manufacturer == 11:
                #Shafi.get_shafi_neman()
                #Lizhka.get_lizhka_product_neman()
                #Komody_tumby.get_komody_tumby_neman()
                Stoly.get_stoly_neman()
                Pcstoly.get_pcstoly_neman()

                 


            if manufacturer == 12:
                Lizhka.get_lizhka_product_estella() #Не оновлюємо
            
                 


            if manufacturer == 13:
                Lizhka.get_lizhka_product_tenero()

                 
            

            if manufacturer == 14:
                Lizhka.get_lizhka_product_arbordrev()
                Komody_tumby.get_komody_tumby_arbordrev()

                 
            

            if manufacturer == 15:
                Matratsy.get_matrasy_emm()

                 


            if manufacturer == 16:
                Matratsy.get_matrasy_eurosleep()

                 

            
            if manufacturer == 17:
                Shafi.get_shafi_mixmebli()
                Myakimebli.get_myakimebli_mixmebli()
                Lizhka.get_lizhka_mixmebli()

                 

            
            if manufacturer == 18:
                Lizhka.get_lizhka_kompanit() #Не перевірено
                Komody_tumby.get_komody_tumby_kompanit()

                 


            if manufacturer == 19:
                Stoly.get_stoly_jam()

                 

            
            if manufacturer == 20:
                Stoly.get_stoly_modul_lux()
                Stiltsi_taburety.get_stiltsi_taburety_modul_lux()

                 


            if manufacturer == 21:
                Myakimebli.get_myaki_mebli_yudin()
                Lizhka.get_lizhka_yudin()
                Kukhonni_kutochky.get_kukhonni_kutochky_yudin()

                 
        

            if manufacturer == 144:
                Lizhka.get_lizhka_product_olimp()
                Komody_tumby.get_komody_tumby_olimp()

                 

            
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
