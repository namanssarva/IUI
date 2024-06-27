from django.db import models
from django.contrib.auth.models import User


class UploadedDocument(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
class User(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null = True,blank = True)