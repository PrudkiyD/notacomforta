from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<category>/<id>', views.product),
    path('sitemap.xml', views.sitemap),
]