from django.urls import path
from . import views

app_name='shoping'

urlpatterns = [
    path('shoping_list/',views.shoping_list,name='shoping_list'),
    path('sell_product',views.sell_product,name='sell_product'),
    path('product_details/<int:product_info_id>/',views.product_details,name='product_details'),
    path('upload_image/<int:image_info_id>',views.upload_image,name='upload_image'),
    path('my_list',views.my_list,name='my_list'),
    path('delete_product/<int:product_id>',views.delete_product,name='delete_product'),
    path('product_update/<int:product_info_id>',views.product_update,name='product_update'),
    path('messaging/<int:product_id>/<int:byer_id>',views.messaging,name='messaging'),
    path('recipients_list/<int:product_id>',views.recipients_list,name='recipients_list'),
    
    path('full_image/<path:image_url>/<str:has_permission>',views.full_image,name='full_image'),
    path('full_image/<path:image_url>/<str:has_permission>/<int:user_id>/<str:user_type>/',views.full_image,name='full_image'),
    path('delete_product_image/<path:image_id>',views.delete_product_image,name='delete_product_image'),
]
