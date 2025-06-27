from django.db import models
from login.models import LoginModel
from django.contrib.auth.models import User

class AddShopModel(models.Model):
    shop_name = models.CharField(max_length=200, verbose_name='دکان کا نام')
    shop_address = models.CharField(max_length=200, verbose_name='پتہ')
    phone = models.CharField(max_length=20, verbose_name='فون نمبر', blank=True, null=True)
    shop_owner = models.ForeignKey(LoginModel, on_delete=models.CASCADE, blank=True, verbose_name='مالک')
    date = models.DateField(auto_now_add=True, verbose_name='تاریخ')
    booking = models.BooleanField(default=True, blank=True, null=True, verbose_name='بکنگ')
    price = models.IntegerField(blank=True, verbose_name='قیمت', default=1000)
    map_link = models.CharField(max_length=2000, verbose_name='نقشہ لنک', null=True, blank=True)
    more_information = models.CharField(max_length=600, verbose_name='مزید معلومات', blank=True, null=True)
    image = models.ImageField(blank=True, null=True, verbose_name='تصویر', upload_to='shop_images',default='default_shop.jpeg')
    def __str__(self):
        return self.shop_name
