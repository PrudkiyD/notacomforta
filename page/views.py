from django.shortcuts import render
from catalog.models import Category
from page.models import Page


def page(request, page_url):
    categorys = Category.objects.prefetch_related('subcategories')
    pages = Page.objects.filter(published=True)
    
    return render(request, 'page.html', {
        'title': pages.filter(slug = page_url).first().h1,
        'content': pages.filter(slug = page_url).first().content,
        'pages':pages,
        'categorys': categorys,
        'canonical':f"https://www.notacomforta.pl.ua/catalog/{page_url}"
    })

