from django.urls import path
from . import views

app_name='payments'

urlpatterns = [
    path('start_payment',views.start_payment,name='start_payment'),
    path('get_trnxn_id/<str:payment_method>',views.get_trnxn_id,name='get_trnxn_id'),
]
