from googletrans import Translator
import re
import os

os.chdir('static\img')
path = os.getcwd()
lib_list = os.listdir(path)


def img_search(img_search, lib_list=lib_list):
    resolt = []
    for i in lib_list:
        match = re.search(img_search, i)
        if match:
            resolt.append(i)

    return resolt


def trans(text):
    translator = Translator().translate(text=text, src='ru', dest='uk')
    return translator.text
