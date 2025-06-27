from django.urls import path
from . import views

app_name='measurements'

urlpatterns = [
    path('add_measurement/<int:customer_id>',views.add_measurement,name='add_measurement'),
]
