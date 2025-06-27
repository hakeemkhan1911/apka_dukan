from django.db import models
from django.contrib.auth.models import User

class FeedbackModel(models.Model):
    rater=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    rating = models.IntegerField()
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating: {self.rating} - {self.created_at}"

class ContactUs(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,verbose_name='Name')
    message=models.CharField(max_length=500,verbose_name='میسج')
    email=models.EmailField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message[0:20]
    
