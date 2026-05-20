from django.urls import path
from . import views

urlpatterns = [
    path('', views.update, name='update'),
    path("discount/", views.discount, name="discount"),

]

