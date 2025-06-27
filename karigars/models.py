from django.db import models
from shops.models import AddShopModel


class RegisterKarigarModel(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='نام')
    phone=models.CharField(max_length=20,verbose_name='فون',blank=True,null=True)
    karigar_shop = models.ForeignKey(AddShopModel, on_delete=models.CASCADE, verbose_name='دکان', blank=True, null=True)
    email = models.CharField(max_length=100, verbose_name='ای میل', null=True)
    address = models.CharField(max_length=150, verbose_name='پتہ')
    password = models.CharField(max_length=100, verbose_name='پاس ورڈ')
    password_again = models.CharField(max_length=100, verbose_name='پاس ورڈ دوبارہ درج کریں')
    experience = models.TextField(verbose_name='اپنے بارے میں', null=True)
    karigar_date = models.DateField(auto_now_add=True, verbose_name='تاریخ')
    fake_id = models.IntegerField(blank=True, null=True, verbose_name='جعلی آئی ڈی')
    status = models.CharField(max_length=20, blank=True, default='karigar', verbose_name='حیثیت')
    image = models.ImageField(verbose_name='تصویر', upload_to='karigar', blank=True, null=True)
    def __str__(self):
        return self.full_name
    
    
