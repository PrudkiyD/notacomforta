from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('information/', include('page.urls')),
    path('catalog/', include('catalog.urls')),
    path('order/', include('order.urls')),
    path('update/', include('update.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),   
]

urlpatterns += static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
urlpatterns += path('', include('main.urls')),