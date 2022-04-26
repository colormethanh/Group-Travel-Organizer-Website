from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.forms import ModelForm
from django import forms


# Create your models here.
class Trip(models.Model):
    name = models.CharField(max_length=200, 
                            validators=[MinLengthValidator(3, "Trip title must be longer than 3 characters")]
                            )
    start_date = models.DateField()
    end_date = models.DateField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200, 
                            validators=[MinLengthValidator(3, "Event title must be longer than 3 characters")]
                            )
    location: models.CharField(max_length=200, blank=True)
    cost: models.DecimalField(decimal_places=2, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    confirmed = models.BooleanField(default=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name

                                


    
