from django import forms
from home.models import Trip, Event

class TripForm(forms.ModelForm):
    
    class Meta:
        model = Trip
        fields = '__all__'
        exclude = ['owner'] 
        widgets = {
            'start_date': forms.DateInput(
                            format=('%Y-%m-%d'),
                            attrs={'class': 'form-control', 
                            'placeholder': 'Select a date',
                            'type': 'date'
              }),
            'end_date': forms.DateInput(
                            format=('%Y-%m-%d'),
                            attrs={'class': 'form-control', 
                            'placeholder': 'Select a date',
                            'type': 'date'
              }),

        }

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        #fields= ['name', 'location', 'cost', 'start_date', 'end_date']
        fields = '__all__'
        exclude= ['confirmed', 'trip']
    
        widgets = {
            'start_date': forms.DateInput(
                            format=('%Y-%m-%d'),
                            attrs={'class': 'form-control', 
                            'placeholder': 'Select a date',
                            'type': 'date'
              }),
            'end_date': forms.DateInput(
                            format=('%Y-%m-%d'),
                            attrs={'class': 'form-control', 
                            'placeholder': 'Select a date',
                            'type': 'date'
              }),
        }
