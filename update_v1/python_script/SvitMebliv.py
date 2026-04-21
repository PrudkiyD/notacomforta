import requests
import openpyxl
from bs4 import BeautifulSoup
import re
import os
import json
from main.models import Seria, Stinka, Stinka_img
from pars.models import File


with open('/home/ay507291/notacomforta.pl.ua/www/pars/src.json', 'r') as f:
    file = json.load(f)

path_dirver = file['src'][0]['path_dirver']
accept = file['src'][1]['accept']
user_agent = file['src'][2]['user-agent']

HEADERS = {
    'accept': accept,
    'user-agent': user_agent
}

HOST = 'https://komfortmebli.com.ua'

path = os.getcwd()


def num_check(text):
    num = ''
    for t in text:
        if t.isdigit():
            num += t
    return num

def lover():
    for m in Stinka.objects.filter(manufacturer_id=2):
        Stinka.objects.filter(id=m.id).update(pars_name = str(m.pars_name).replace(' ', '').lower())
        print('--> ', m.pars_name)

    for m in Seria.objects.filter(manufacturer_id=2):
        Seria.objects.filter(id=m.id).update(pars_name = str(m.pars_name).replace(' ', '').lower())
        print('--> ', m.pars_name)
