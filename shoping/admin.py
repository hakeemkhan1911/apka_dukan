from django.contrib import admin
from .models import SellProductModel,ImageModel,SellerByer,MessagesModel

admin.site.register(SellProductModel)
admin.site.register(ImageModel)
admin.site.register(SellerByer)
admin.site.register(MessagesModel)

# Register your models here.
