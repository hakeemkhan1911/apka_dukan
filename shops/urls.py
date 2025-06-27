from django.urls import path
from . import views

app_name='shops'

urlpatterns = [
    path('add_shop',views.add_shop,name='add_shop'),
    path('update_shop/<int:shop_id>',views.update_shop,name='update_shop'),
    path('delete_shop/<int:shop_id>',views.delete_shop,name='delete_shop'),
    path('shop_details/<int:shop_id>',views.shop_details,name='shop_details'),
    path('shop_details/<int:shop_id>/<str:status>',views.shop_details,name='shop_details'),
    path('update_shop_photo/<int:shop_id>',views.update_shop_photo,name='update_shop_photo'),
    
    path('booking/<int:shop_id>',views.booking,name='booking'),
    path('google_map/<int:shop_id>',views.google_map,name='google_map'),
    path('request_recived/<int:shop_id>',views.request_recived,name='request_recived'),
    path('delete_request/<int:shop_id>',views.delete_request,name='delete_request'),
    path('request_accept/<int:r_id>/',views.request_accept,name='request_accept'),
    path('my_karigar/<int:shop_id>',views.my_karigar,name='my_karigar'),
    
    
    path('karigar_info/<int:k_id>',views.karigar_info,name='karigar_info'),
    path('karigar_info/<int:k_id>/<int:shop_id>',views.karigar_info,name='karigar_info'),
    path('leave_shop/<int:shop_id>',views.leave_shop,name='leave_shop'),
    path('leave_shop/<int:shop_id>/<int:krgr_id>',views.leave_shop,name='leave_shop'),
    path('request_karigar/<int:karigar_id>',views.request_karigar,name='request_karigar'),
    path('delete_karigar_request/<int:karigar_fake_id>',views.delete_karigar_request,name='delete_karigar_request'),
    
    path('rate_shop/<int:shop_id>/<int:customer_id>/',views.rate_shop,name='rate_shop'),
]
