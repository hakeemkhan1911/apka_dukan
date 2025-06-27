from django.db import models
from shops.models import AddShopModel
from karigars.models import RegisterKarigarModel

requesters=[
    ('shop','shop'),
    ('karigar','karigar'),
    ]

class AddRequest(models.Model):
    karigar = models.ForeignKey(RegisterKarigarModel,on_delete=models.CASCADE,blank=True)
    shop = models.ForeignKey(AddShopModel,on_delete=models.CASCADE,blank=True)
    requester=models.CharField(max_length=30,choices=requesters,blank=True,null=True)
    status = models.CharField(max_length=20,blank=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.karigar.full_name
