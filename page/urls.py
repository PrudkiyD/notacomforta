from django.urls import path
from . import views

urlpatterns = [
    path('<page_url>', views.page),
    ]