from django.urls import path
from . import views

app_name='orders'

urlpatterns = [
    path('add_order/<int:customer_id>',views.add_order,name='add_order'),
    path('order_details/<int:customer_id>',views.order_details,name='order_details'),
    path('update_order/<int:order_id>',views.update_order,name='update_order'),
    path('delete_order/<int:order_id>',views.delete_order,name='delete_order'),
    path('new_order/<int:order_id>',views.new_order,name='new_order'),
    
]
