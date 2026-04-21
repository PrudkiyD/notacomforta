from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('cart/create-key', views.createkey),
    path('cart/<customer_key>', views.cart),
    path('cart/add/<customer_key>/<product_id>/<price_id>', views.add_to_cart),
    path('cart/minus/<customer_key>/<product_id>/<price_id>', views.minus),
    path('cart/quantity/<customer_key>/<product_id>/<price_id>/<quantity>', views.quantity),
    path('successful/', views.successful),
    path('successful/<order_id>', views.successful_track),
    path('track', views.track)
]