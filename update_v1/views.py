from itertools import product
from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse
from main.models import Seria, Stinka, Stinka_img
from komodytumby.models import Komodytumby, Komodytumby_img

from pcstoly.models import Pcstoly, Pcstoly_img
from lizhka.models import Bed, Bed_img, Bed_size
from matrasy.models import Matrasy, Matrasy_img, Matrasy_size
from kyhni.models import Kyhni, Kyhni_img, Manufacturer

from myakimebli.models import Myakimebli, Myakimebli_img, Product_myakimebli
from komodytumby.models import Komodytumby, Komodytumby_img
from stoly.models import Stoly, Stoly_img, Stoly_size
from pcstoly.models import Pcstoly, Pcstoly_img, Pcstoly_size
from stiltsi_taburety.models import Stiltsi_taburety, Stiltsi_taburety_size, Stiltsi_taburety_img
from kukhonni_kutochky.models import Kukhonni_kutochky, Kukhonni_kutochky_img, Kukhonni_kutochky_size
import json


from pars.python_script import Kyhni
from pars.python_script import Shafi
from pars.python_script import Myakimebli
from pars.python_script import Vitalni
from pars.python_script import Peredpokoi
from pars.python_script import Spalni
from pars.python_script import Dytyachi
from pars.python_script import Lizhka
from pars.python_script import Matratsy
from pars.python_script import Komody_tumby
from pars.python_script import Stoly
from pars.python_script import Pcstoly
from pars.python_script import Stiltsi_taburety
from pars.python_script import Kukhonni_kutochky
from pars.python_script import Dribnytsi
from pars.python_script import SvitMebliv
from pars.python_script import Other
from pars.python_script import Matrolux_module
from pars.python_script import dev


from pars.interest import kyhni
from pars.interest import shafi
from pars.interest import myakimebli
from pars.interest import komodytumby
from pars.interest import bed
from pars.interest import matrasy
from pars.interest import stoly
from pars.interest import pcstoly
from pars.interest import stiltsi_taburety
from pars.interest import kukhonni_kutochky
from pars.interest import vitalni


def pars(request):

    #dev.dev()
    
    pars = request.POST.get('pars')
    man = request.POST.get('man')
    interest = request.POST.get('interest')
    category = request.POST.get('category')
    id_list = request.POST.get('id_list')

    #Перенесено
    if pars == '1':
        if man == '1':
            Kyhni.get_seria_komfortmebli() #Перевірено
        if man == '2':
            Kyhni.get_seri_svitmebliv() #Перевірено

    #Перенесено
    if pars == '2':
        if man == '1':
            Shafi.get_prod_komfortmebli() #Перевірено
        if man == '4':
            Shafi.get_link_matrolux() #Перевірено
        if man == '5':
            Shafi.get_products_fenix() #Перевірено
        if man == '11':
            Shafi.get_shafi_neman() #Перевірено

        if man == '17':
            Shafi.get_shafi_mixmebli()
    
    #Перенесено
    if pars == '3':
        if man == '4':
            Myakimebli.get_myaki_mebli_matrolux() #Перевірено
        if man == '6':
            Myakimebli.get_products_richman() #Перевірено

        if man == '17':
            Myakimebli.get_myakimebli_mixmebli()

    #---
    if pars == '4':
        if man == '1':
            Vitalni.get_vitalni_products_comfortmebli() #Перевірено
            Peredpokoi.get_peredpokoi_products_comfortmebli() #Перевірено
            Spalni.get_spalni_products_comfortmebli() #Перевірено
            Dytyachi.get_dytyachi_products_comfortmebli() #Перевірено

        if man == '2':
            Vitalni.get_vitalni_products_svitmebliv() #Перевірено
            Peredpokoi.get_peredpokoi_products_svitmebliv() #Перевірено
            Spalni.get_spalni_products_svitmebliv() #Перевірено
            Dytyachi.get_dytyachi_products_svitmebliv() #Перевірено

        if man == '4':
            Matrolux_module.get_stinka_matrolux()

        if man == '7':
            Vitalni.get_vitalni_products_lion() #Перевірено
            Spalni.get_spalni_products_lion() #Перевірено
            Dytyachi.get_dytyachi_products_lion() #Перевірено

        if man == '8':
            Vitalni.get_vitalni_products_BMK() #Перевірено 
        
        if man == '9':
            Vitalni.get_vitalni_products_gerbor() #Перевірено
            Peredpokoi.get_peredpokoi_products_gerbor() #Перевірено
            
        if man == '10':
            Vitalni.get_vitalni_products_everest() #Перевірено
            Peredpokoi.get_peredpokoi_products_everest() #Перевірено
            Spalni.get_spalni_products_everest() #Перевірено

        if man == '11':
            Spalni.get_spalni_products_neman() #Перевірено

        if man == '17':
            Vitalni.get_vitalni_mixmebli()

        if man == '18':
            Peredpokoi.get_peredpokoi_products_kompanit() #Перевірено

    if pars == '5':
        if man == '1':
            Lizhka.get_lizhka_komfortmebli() #Перевірено
        if man == '4':
            Lizhka.get_lizhka_products_matrolux() #Перевірено
        if man == '14':
            Lizhka.get_lizhka_product_arbordrev() #Перевірено
        if man == '10':
            Lizhka.get_lizhka_product_everest() #Перевірено
        if man == '6':
            Lizhka.get_lizhka_product_richman() #Перевірено
        if man == '2':
            Lizhka.get_lizhka_product_svitmebliv() #Перевірено
        if man == '7':
            Lizhka.get_lizhka_product_lion() #Перевірено
        if man == '144':
            Lizhka.get_lizhka_product_olimp() #Перевірено
        if man == '11':
            Lizhka.get_lizhka_product_neman() #Перевірено
        if man == '13':
            Lizhka.get_lizhka_product_tenero() #Перевірено
        if man == '12':
            Lizhka.get_lizhka_product_estella() #Не оновлюємо
        if man == '18':
            Lizhka.get_lizhka_kompanit() #Перевірено
        if man == '17':
            Lizhka.get_lizhka_mixmebli()

    if pars == '6':
        if man == '4':
            Matratsy.get_matrasy_matrolux() #Перевірено
        if man == '15':
            Matratsy.get_matrasy_emm() #Перевірено
        if man == '16':
            Matratsy.get_matrasy_eurosleep() #Перевірено

    if pars == '7':
        if man == '1':
            Komody_tumby.get_komody_tumby_comfortmebli()
        if man == '4':
            Komody_tumby.get_komody_tumby_matrolux() #Перевірено
        if man == '10':
            Komody_tumby.get_komody_tumby_everest() #Перевірено
        if man == '14':
            Komody_tumby.get_komody_tumby_arbordrev() #Перевірено
        if man == '7':
            Komody_tumby.get_komody_tumby_lion() #Перевірено
        if man == '2':
            Komody_tumby.get_komody_tumby_svitmebliv() #Перевірено
        if man == '11':
            Komody_tumby.get_komody_tumby_neman() #Перевірено
        if man == '144':
            Komody_tumby.get_komody_tumby_olimp() #Перевірено
        if man == '18':
            Komody_tumby.get_komody_tumby_kompanit() #Перевірено

    if pars == '8':
        if man == '14':
            Stoly.get_stoly_arbordrev() #Перевірено
        if man == '10':
            Stoly.get_stoly_everest() #Перевірено
        if man == '18':
            Stoly.get_stoly_kompanit()
        if man == '19':
            Stoly.get_stoly_jam() #Перевірено
        if man == '11':    
            Stoly.get_stoly_neman() #Перевірено
        if man == '7':
            Stoly.get_stoly_lion() #Перевірено
        if man == '13':    
            Stoly.get_stoly_tenero() #Перевірено
        if man == '20':    
            Stoly.get_stoly_modul_lux() #Перевірено
        if man == '6':    
            Stoly.get_stoly_richman() #Перевірено
        if man == '17':    
            Stoly.get_stoly_mixmebli()
        if man == '4':
            Stoly.get_stoly_matrolux()

    if pars == '9':
        if man == '1':
            Pcstoly.get_pcstoly_comfortmebli()
        if man == '4':
            Pcstoly.get_pcstoly_matrolux() #Перевірено
        if man == '18':
            Pcstoly.get_pcstoly_kompanit()
        if man == '10':    
            Pcstoly.get_pcstoly_everest() #Перевірено
        if man == '7':    
            Pcstoly.get_pcstoly_lion() #Перевірено
        if man == '2':    
            Pcstoly.get_pcstoly_svit_mebliv() #Перевірено
        if man == '11':    
            Pcstoly.get_pcstoly_neman()

        if man == '17':   
            Pcstoly.get_pcstoly_mixmebli() 

    if pars == '10':
        if man == '14':
            Stiltsi_taburety.get_stiltsi_taburety_arbordrev() #Перевірено
        if man == '18':    
            Stiltsi_taburety.get_stiltsi_taburety_kompanit()
        if man == '13':    
            Stiltsi_taburety.get_stiltsi_taburety_tenero()
        if man == '20':    
            Stiltsi_taburety.get_stiltsi_taburety_modul_lux() #Перевірено
        if man == '6':    
            Stiltsi_taburety.get_stiltsi_taburety_richman() #Перевірено
        if man == '7':    
            Stiltsi_taburety.get_stiltsi_taburety_lion() #Перевірено
        if man == '17':    
            Stiltsi_taburety.get_stiltsi_taburety_mixmebli()

    if pars == '11':
        if man == '18':
            Kukhonni_kutochky.get_kukhonni_kutochky_kompanit() #Перевірено
        if man == '7':
            Kukhonni_kutochky.get_kukhonni_kutochky_lion() #Перевірено
        
        if man == '17':
            Kukhonni_kutochky.get_kukhonni_kutochky_mixmebli()

    if pars == '12':
        if man == '11':
            Other.get_other_neman()

    if pars == '13':
        pass

    if pars == '14':
        if man:
            Dribnytsi.get_dribnytsi_mixmebli()

    else:
        pass

    #Корегування ціни
    if category == 'kyhni':
        kyhni.interest(interest, str(id_list).split(';'))
    
    if category == 'shafi':
        shafi.interest(interest, str(id_list).split(';'))

    if category == 'myakimebli':
        myakimebli.interest(interest, str(id_list).split(';'))

    if category == 'stinka':
        vitalni.interest(interest, str(id_list).split(';'))

    if category == 'bed':
        bed.interest(interest, str(id_list).split(';'))

    if category == 'matrasy':
        matrasy.interest(interest, str(id_list).split(';'))

    if category == 'komodytumby':
        komodytumby.interest(interest, str(id_list).split(';'))

    if category == 'stoly':
        stoly.interest(interest, str(id_list).split(';'))

    if category == 'pcstoly':
        pcstoly.interest(interest, str(id_list).split(';'))

    if category == 'stiltsi_taburety':
        stiltsi_taburety.interest(interest, str(id_list).split(';'))

    if category == 'kukhonni_kutochky':
        kukhonni_kutochky.interest(interest, str(id_list).split(';'))


    if pars == '0' and man == '0':
        pass

    context = {'back': pars}
    return render(request, 'pars/pars.html', {'context':context})