
from django.db import models 
from django.contrib.auth.models import User

# Create your models here.
class CRM(models.Model):
    ROLE = (
        ('BDA', 'Business Development Executive'),
        ('CS', 'Customer Support'),
        ('IS', 'Inside Sales'),
        ('CW', 'Content Writing'),
        ('DM', 'Digital Marketing'),
    )
    
    role = models.CharField(max_length=5, choices=ROLE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    place = models.CharField(max_length=60)
    phone = models.BigIntegerField()