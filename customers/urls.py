from django.urls import path
from . import views

app_name='customers'

urlpatterns = [
    path('add_customer/<int:shop_id>',views.add_customer,name='add_customer'),
    path('add_customer/<int:shop_id>/<int:deleted>',views.add_customer,name='add_customer'),
    path('customer_details/<int:customer_id>',views.customer_details,name='customer_details'),
    path('update_customer/<int:customer_id>',views.update_customer,name='update_customer'),
    path('delete_customer/<int:customer_id>',views.delete_customer,name='delete_customer'),
    path('login_customer/<int:shop_id>',views.login_customer,name='login_customer'),
    path('share_customer_details/<int:customer_id>',views.share_customer_details,name='share_customer_details'),
    
]
