from django.urls import path
from . import views

app_name='requests'

urlpatterns = [
    path('place_request/',views.place_request,name='place_request'),
    
]
