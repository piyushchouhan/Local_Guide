# Create your models here.
# models.py
from django.db import models
from localguides.models import User, Guide

class Meeting_Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
