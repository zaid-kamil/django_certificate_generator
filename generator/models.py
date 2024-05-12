from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    
class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    name = models.CharField(max_length=100) 
    date = models.DateField(default=datetime.now)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, null=True, blank=True)
    hash = models.CharField(max_length=255, null=True, blank=True)
    previous_hash = models.CharField(max_length=255, null=True, blank=True, default='fd2959c16427a12461b33f25224f1675015dd0df935074f0604d0dc927fb87cd')
    file = models.FileField(upload_to='certificates', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Report(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    issue = models.TextField()
    certificate_id = models.IntegerField(help_text='Enter the certificate ID if this report is about a certificate eg., 941')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


