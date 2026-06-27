from celery import shared_task
from .models import TaskExecution
import time
from django.utils import timezone
import logging
from .script import Kyhni, Shafi, Myakimebli, Lizhka, \
                    Matratsy, Komody_tumby, Peredpokoi, Vitalni, Spalni, \
                    Dytyachi, Matrolux_module, Stoly, Pcstoly, \
                    Kukhonni_kutochky, Stiltsi_taburety, RichmanUpdate


logger = logging.getLogger(__name__)

@shared_task
def update_task(manufacturer):

    if manufacturer == 1:
        task_status = TaskExecution.objects.create(
            name="Комфорт меблі",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Kyhni.get_seria_komfortmebli()
            Shafi.get_prod_komfortmebli()
            Lizhka.get_lizhka_komfortmebli()
            Vitalni.get_vitalni_products_comfortmebli()
            Spalni.get_spalni_products_comfortmebli()
            Peredpokoi.get_peredpokoi_products_comfortmebli()
            Dytyachi.get_dytyachi_products_comfortmebli()
            Komody_tumby.get_komody_tumby_comfortmebli()
            Pcstoly.get_pcstoly_comfortmebli()  

            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()

    if manufacturer == 2:
        task_status = TaskExecution.objects.create(
            name="Світ Меблів",
            status=TaskExecution.Status.PENDING,
        )
        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            #Kyhni.get_seri_svitmebliv() змінився сайт потрібен новий парсер
            Shafi.get_shafi_svitmebliv()
            Shafi.get_stelazhi_svitmebliv()
            Lizhka.get_lizhka_product_svitmebliv()
            Vitalni.get_vitalni_products_svitmebliv()
            Peredpokoi.get_peredpokoi_products_svitmebliv()
            Spalni.get_spalni_products_svitmebliv()
            Dytyachi.get_dytyachi_products_svitmebliv()
            Komody_tumby.get_komody_tumby_svitmebliv()

        
            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()

    if manufacturer == 4:
        task_status = TaskExecution.objects.create(
            name="Матролюкс",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()
        
            Shafi.get_link_matrolux()
            Myakimebli.get_myaki_mebli_matrolux()
            Lizhka.get_lizhka_products_matrolux()
            Matrolux_module.get_stinka_matrolux()
            Matratsy.get_matrasy_matrolux()
            Komody_tumby.get_komody_tumby_matrolux()
            Stoly.get_stoly_matrolux()
            Pcstoly.get_pcstoly_matrolux()

            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
            
    if manufacturer == 5:
        task_status = TaskExecution.objects.create(
            name="Фенікс Мблі",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Shafi.get_products_fenix()

            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()

    if manufacturer == 6:
        task_status = TaskExecution.objects.create(
            name="Richman",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            RichmanUpdate.get_products_richman()

            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()

    if manufacturer == 7:
        task_status = TaskExecution.objects.create(
            name="Ліон",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Lizhka.get_lizhka_product_lion() #Немає файла для оновлення
            Komody_tumby.get_komody_tumby_lion()

            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Оновлення не перевірине. Відсутній файл оновлення для ліжок."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка. Оновлення не перевірине. Відсутній файл оновлення для ліжок."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()

    if manufacturer == 8:
        task_status = TaskExecution.objects.create(
            name="БМК",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()
            
            Vitalni.get_vitalni_products_bmk()
        
            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()

    if manufacturer == 9:
        task_status = TaskExecution.objects.create(
            name="Гербор",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Vitalni.get_vitalni_products_gerbor()
            Peredpokoi.get_peredpokoi_products_gerbor()
            
            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()

    if manufacturer == 10:
        task_status = TaskExecution.objects.create(
            name="Еверест",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Lizhka.get_lizhka_product_everest()
            Komody_tumby.get_komody_tumby_everest()
        
            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
     
    if manufacturer == 11:
        task_status = TaskExecution.objects.create(
            name="Неман",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            #Shafi.get_shafi_neman()
            #Lizhka.get_lizhka_product_neman()
            #Komody_tumby.get_komody_tumby_neman()
            Stoly.get_stoly_neman()
            Pcstoly.get_pcstoly_neman()

            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
      
    if manufacturer == 12:
        task_status = TaskExecution.objects.create(
            name="Естела",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Lizhka.get_lizhka_product_estella() #Не оновлюємо
            
            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Товари не оновлюються."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка. Товари не оновлюються."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
        
    if manufacturer == 13:
        task_status = TaskExecution.objects.create(
            name="Тенеро",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Lizhka.get_lizhka_product_tenero()
        
            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
         
    if manufacturer == 14:
        task_status = TaskExecution.objects.create(
            name="Arbor Drev",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Lizhka.get_lizhka_product_arbordrev()
            Komody_tumby.get_komody_tumby_arbordrev()

            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
       
    if manufacturer == 15:
        task_status = TaskExecution.objects.create(
            name="EMM",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()
            
            Matratsy.get_matrasy_emm()

            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
  
    if manufacturer == 16:
        task_status = TaskExecution.objects.create(
            name="Eurosleep",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Matratsy.get_matrasy_eurosleep()
        
            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
       
    if manufacturer == 17:
        task_status = TaskExecution.objects.create(
            name="Мікс меблі",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Shafi.get_shafi_mixmebli()
            Myakimebli.get_myakimebli_mixmebli()
            Lizhka.get_lizhka_mixmebli()
        
            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
       
    if manufacturer == 18:
        task_status = TaskExecution.objects.create(
            name="Компаніт",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Kukhonni_kutochky.get_kukhonni_kutochky_kompanit()
            Lizhka.get_lizhka_kompanit()
            Komody_tumby.get_komody_tumby_kompanit()

            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
        
    if manufacturer == 19:
        task_status = TaskExecution.objects.create(
            name="Jam",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()


            Stoly.get_stoly_jam()

            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено. Оновлення не пропускає бот. В процесі вирішення."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка. Оновлення не пропускає бот. В процесі вирішення."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
        
    if manufacturer == 20:
        task_status = TaskExecution.objects.create(
            name="Модуль Люкс",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Stoly.get_stoly_modul_lux()
            Stiltsi_taburety.get_stiltsi_taburety_modul_lux()
        
            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
           
    if manufacturer == 21:
        task_status = TaskExecution.objects.create(
            name="Юдін",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Myakimebli.get_myaki_mebli_yudin()
            Lizhka.get_lizhka_yudin()
            Kukhonni_kutochky.get_kukhonni_kutochky_yudin()
        
            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()
            
    if manufacturer == 144:
        task_status = TaskExecution.objects.create(
            name="Олімп",
            status=TaskExecution.Status.PENDING,
        )

        try:
            task_status.status = TaskExecution.Status.STARTED
            task_status.result = f"Розпочаслося ..."
            task_status.started_at = timezone.now()
            task_status.save()

            Lizhka.get_lizhka_product_olimp()
            Komody_tumby.get_komody_tumby_olimp()
        
            task_status.status = TaskExecution.Status.SUCCESS
            task_status.result = f"Завершено."
            task_status.finished_at = timezone.now()
            task_status.save()

        except Exception as ex:
            task_status.status = TaskExecution.Status.FAILED
            task_status.result = f"Сталася помилка."
            task_status.error = ex
            task_status.finished_at = timezone.now()
            task_status.save()