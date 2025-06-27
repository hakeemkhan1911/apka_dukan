from django.db import models
from shops.models import AddShopModel

class AddCustomerModel(models.Model):
    shop = models.ForeignKey(AddShopModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='دکان')
    customer_name = models.CharField(max_length=100, verbose_name='نام')
    customer_phone = models.CharField(max_length=20, verbose_name='فون نمبر')
    customer_address = models.CharField(max_length=150, verbose_name='پتہ')
    password = models.CharField(max_length=100, verbose_name='پاس ورڈ')
    serial_number = models.IntegerField(verbose_name='سیریل نمبر')
    date_time = models.DateField(auto_now_add=True, verbose_name='تاریخ')
    def __str__(self):
        return self.customer_name

class Review(models.Model):
    shop = models.ForeignKey(AddShopModel, on_delete=models.CASCADE, related_name='reviews') 
    customer = models.ForeignKey(AddCustomerModel, on_delete=models.CASCADE)
    rating = models.IntegerField() 
    comment = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.customer_name} - {self.rating} Stars"