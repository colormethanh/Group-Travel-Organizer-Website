from django import forms
from home.models import Trip, Event, Comment, Photos


class TripForm(forms.ModelForm):
    
    class Meta:
        model = Trip
        fields = '__all__'
        exclude = ['owner', 'members', 'voters'] 
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'Your cool trip name here!',
                    'id': 'name'
            }),
            'key': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'A special trip key',
                    'id': 'key'
            }),
            'start_date': forms.DateInput(
                            format=('%Y-%m-%d'),
                            attrs={'class': 'form-control', 
                            'placeholder': 'Select a date',
                            'type': 'date',
                            'id': 'start_date'
            }),
            'end_date': forms.DateInput(
                            format=('%Y-%m-%d'),
                            attrs={'class': 'form-control', 
                            'placeholder': 'Select a date',
                            'type': 'date',
                            'id': 'end_date',
              }),
        }

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'
        exclude= ['confirmed', 'trip', 'voters', 'votes']
    
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'What kind of event?',
                    'id': 'name'
            }),
            'location': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': " Where's it going to be? ",
                    'id': 'location'
            }),
            'cost': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'amount in dollars'
            }),
            'start_date': forms.DateInput(
                            format=('%Y-%m-%d'),
                            attrs={
                            'class': 'form-control', 
                            'placeholder': 'Select a date',
                            'type': 'date'
              }),
            'end_date': forms.DateInput(
                            format=('%Y-%m-%d'),
                            attrs={
                            'class': 'form-control', 
                            'placeholder': 'Select a date',
                            'type': 'date',
                            'id': 'start_date'
              }),
        }

class TripJoinForm(forms.Form):
    trip_key = forms.CharField(widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder':'Trip Key here',
                                        'id':'trip_key'
                                    }),
                                max_length=10,
                                help_text='Enter Trip Key to join'
                                ) 

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields='__all__'
        exclude=['owner', 'trip', 'created_at']

class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photos
        fields = '__all__'
        exclude=['owner','trip','event']

        widgets={
            'image':forms.ClearableFileInput(
                    attrs={
                        'class': 'form-control',
                        'type':'file',
                        'id':'formphoto',
                    }
            )}