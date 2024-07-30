from django.db import models
from localguides.models import Guide

# Create your models here.
class Availability(models.Model):
    local_guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    availability_date = models.DateField()
    is_booked = models.BooleanField(default=False)
