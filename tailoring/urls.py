from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' ,include('home.urls')),
    path('login' ,include('login.urls')),
    path('customers' ,include('customers.urls')),
    path('measurements' ,include('measurements.urls')),
    path('shops' ,include('shops.urls')),
    path('orders',include('orders.urls')),
    path('karigars',include('karigars.urls')),
    path('shoping',include('shoping.urls')),
    path('payments',include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
