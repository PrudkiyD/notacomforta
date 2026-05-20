from django.urls import path
from . import views
from . import tools

urlpatterns = [
    #path('dev/import', tools.import_data),
    #path('dev/delete', tools.delete),
    #path('dev/editimg', tools.editimg),
    #path('dev/edithttp', tools.edithttp),
    #path('dev/editimgmedia', tools.editimgmedia),
    #path('dev/shafi', tools.shafi),
    #path('dev/matras', tools.matras),
    #path('dev/editkyhni', tools.editkyhni),
    #path('dev/encodedimg', tools.encodedimg),
    #path('dev/img', tools.img),
    #path('dev/convertimg', tools.convertimg),

    #path('dev/test', tools.test),
    
    path('', views.catalog),
    path('product/<product_id>', views.product),
    path('search', views.search),
    path('sale', views.sale),
    path('product/<product_id>', views.product),
    path('<category>', views.category),
    path('<category>/<subcategory>', views.category),
    
]