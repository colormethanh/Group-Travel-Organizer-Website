from datetime import datetime
from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.forms import ModelForm
from django import forms
import datetime
from django.core.exceptions import ValidationError

def date_validator(value):
    if value < datetime.date.today():
        raise ValidationError("Date cannot be in the past!")
    else:
        return value


# Create your models here.
class Trip(models.Model):
    name = models.CharField(max_length=200, 
                            validators=[MinLengthValidator(3, "Trip title must be longer than 3 characters")]
                            )
    start_date = models.DateField(validators=[date_validator])
    end_date = models.DateField(validators=[date_validator])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Event(models.Model):
    name = models.CharField(max_length=200, 
                            validators=[MinLengthValidator(3, "Event title must be longer than 3 characters")]
                            )
    location= models.CharField(max_length=200, null=True)
    cost= models.DecimalField( max_digits=4 , decimal_places=2, default = 0)
    start_date = models.DateField(validators=[date_validator], null=True)
    end_date = models.DateField(validators=[date_validator], null=True)
    confirmed = models.BooleanField(default=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True) 

    def __str__(self):
        return self.name

                                


    
