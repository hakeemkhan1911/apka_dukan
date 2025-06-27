from django.db import models
from django.contrib.auth.models import User

PRODUCTS = {
    ('mobile', 'موبائل'),
    ('car', 'کار'),
    ('statinory', 'اسٹیشنری'),
    ('fashion', 'فیشن'),
    ('fabrics', 'کپڑے'),
    ('electronics', 'الیکٹرانکس'),
    ('furniture', 'فرنیچر'),
    ('books', 'کتابیں'),
    ('toys', 'کھلونے'),
    ('kitchen', 'کچن آئٹمز'),
    ('appliances', 'آلات'),
    ('beauty', 'خوبصورتی'),
    ('sports', 'کھیل'),
    ('vehicles', 'گاڑیاں'),
    ('property', 'جائیداد'),
    ('services', 'سروسز'),
    ('accessories', 'لوازمات'),
}
CONDITION = {
    ('New', 'نیا'),
    ('Like New', 'نیا جیسا'),
    ('Used Excellent condition', 'استعمال شدہ - بہترین حالت'),
    ('Used Good condition', 'استعمال شدہ - اچھی حالت'),
    ('Not working', 'خراب'),
}

class SellProductModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='مالک')
    name = models.CharField(max_length=200, verbose_name='نام', blank=True, null=True)
    condition = models.CharField(max_length=40, verbose_name='حالت', default='New', null=True, choices=CONDITION)
    category = models.CharField(max_length=20, choices=PRODUCTS, default='mobile', blank=True, null=True, verbose_name='زمرہ')
    price = models.IntegerField(verbose_name='قیمت')
    location=models.CharField(max_length=200,verbose_name='لوکیشن',blank=True,null=True)
    date = models.DateField(auto_now_add=True, verbose_name='تاریخ')
    details = models.TextField(null=True, blank=True, verbose_name='تفصیلات')

    def __str__(self):
        return self.owner.username
class ImageModel(models.Model):
    product_info = models.ForeignKey(SellProductModel,on_delete=models.CASCADE,blank=True)
    image=models.ImageField(verbose_name='Image',upload_to='product_images',default='im.jpg')
    def __str__(self):
        return self.product_info.name

class SellerByer(models.Model):
    byer=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name='byer')
    seller=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name='seller')
    product=models.ForeignKey(SellProductModel,on_delete=models.CASCADE,blank=True,related_name='product')
    def __str__(self):
        return self.seller.username

class MessagesModel(models.Model):
    message_header=models.ForeignKey(SellerByer,on_delete=models.CASCADE,blank=True,related_name='message_header')
    sender=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name='sender')
    reciver=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name='reciver')
    message=models.CharField(max_length=1000,verbose_name='Message')
    date=models.DateTimeField(auto_now_add=True)
    byer_read=models.BooleanField(default=False)
    seller_read= models.BooleanField(default=False)
    def __str__(self):
        return self.sender.username
    
    
    