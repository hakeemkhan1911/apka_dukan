from django.db import models
from django.conf import settings

PLAN_CHOICES = [
    ('monthly', ' Monthly - Rs.200'),
]

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tid = models.CharField(max_length=20, unique=True,blank=True,null=True)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='monthly',blank=True,null=True)
    payment_method = models.CharField(max_length=20,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user.username)+'----'+str(self.is_verified)
    class Meta:
        ordering=['is_verified','created_at']