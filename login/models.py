from django.db import models
from django.utils import timezone

class LoginModel(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='پہلا نام')
    last_name = models.CharField(max_length=150, verbose_name='آخری نام')
    full_name = models.CharField(max_length=300, blank=True, verbose_name='پورا نام')
    address = models.CharField(max_length=150, verbose_name='پتہ')
    phone = models.CharField(max_length=20, verbose_name='فون نمبر')
    email = models.EmailField(verbose_name='ای میل', blank=True)
    password = models.CharField(max_length=100, verbose_name='پاس ورڈ')
    password_again = models.CharField(max_length=100, verbose_name='پاس ورڈ دوبارہ درج کریں')
    status = models.CharField(max_length=20, blank=True, default='shop_keeper', verbose_name='حیثیت')
    fake_id = models.IntegerField(blank=True, verbose_name='جعلی آئی ڈی')
    date = models.DateField(auto_now_add=True, verbose_name='تاریخ')
    image = models.ImageField(upload_to='users_profile', verbose_name='تصویر', blank=True, null=True)
    def __str__(self):
        return self.full_name


class OTP(models.Model):
    email = models.CharField(max_length=200, unique=True)  # Store phone number (or email)
    otp = models.CharField(max_length=6)  # 6-digit OTP
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for expiry
    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)  # Expiry in 5 min
