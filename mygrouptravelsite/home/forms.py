from django import forms
from home.models import Trip, Event, Comment

class TripForm(forms.ModelForm):
    
    class Meta:
        model = Trip
        fields = '__all__'
        exclude = ['owner', 'members'] 
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

class TripJoinForm(forms.Form):
    trip_key = forms.CharField(max_length=10,
                                help_text='Enter Trip Key to join'
                                ) 

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields='__all__'
        exclude=['owner', 'trip', 'created_at']