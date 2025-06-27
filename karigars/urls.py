from django.urls import path
from . import views

app_name='karigars'

urlpatterns = [
    path('register_karigar',views.register_karigar,name='register_karigar'),
    path('update_karigar',views.update_karigar,name='update_karigar'),
    path('login_karigar',views.login_karigar,name='login_karigar'),
    path('delete_karigar',views.delete_karigar,name='delete_karigar'),
    path('all_karigars',views.all_karigars,name='all_karigars'),
    
]
