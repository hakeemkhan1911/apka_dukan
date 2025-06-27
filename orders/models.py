from django.db import models
from customers.models import AddCustomerModel

class AddOrderModel(models.Model):
    customer = models.ForeignKey(AddCustomerModel, on_delete=models.CASCADE, blank=True, verbose_name='کسٹمر')
    previous = models.IntegerField(verbose_name='پرانا بقایا', default=0)
    total_price = models.IntegerField(verbose_name='کل قیمت', default=0)
    advance = models.IntegerField(verbose_name='ایڈوانس', default=0)
    remining = models.IntegerField(verbose_name='بقایا', default=0)
    order_number = models.IntegerField(verbose_name='آرڈر نمبر', default=0)
    delivery_date = models.DateField(verbose_name='ترسیل کی تاریخ')
    details = models.CharField(max_length=400, verbose_name='تفصیلات', blank=True, null=True, default=None)
    date = models.DateField(auto_now_add=True, verbose_name='تاریخ')

    def __str__(self):
        return self.customer.customer_name