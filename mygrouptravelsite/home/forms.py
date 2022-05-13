from datetime import datetime
from tracemalloc import start
from xml.dom import ValidationErr
from django import forms
from home.models import Group, Event, Comment, Photos


class GroupForm(forms.ModelForm):
    
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['owner', 'members', 'voters'] 
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'Your cool group name here!',
                    'id': 'name'
            }),
            'key': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'A special group key',
                    'id': 'key'
            }),
            'description': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'Every group needs a desciption right? :D',
                    'id': 'description',
            }),
        }

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'
        exclude= ['confirmed', 'group', 'voters', 'votes']
    
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'What kind of event?',
                    'id': 'name'
            }),
            'description': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'Every event needs a desciption right? :D',
                    'id': 'description',
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
    def clean(self):
        cd = self.cleaned_data
        e_start_date = cd.get("start_date")
        e_end_date = cd.get("end_date")

        if e_end_date < e_start_date:
            raise forms.ValidationError("End Date cannot be before start date!")

        for event in Event.objects.filter(start_date__gte = datetime.now(), confirmed = True):
            print(event)
            event_dates = event.get_dates_range(e_start_date, e_end_date)
            dates = event.get_dates_range(event.start_date, event.end_date)
            print(f'Event dates: {event_dates}')
            print(f'Dates: {dates}')
            for date in event_dates:
                if date in dates:
                    raise forms.ValidationError("Submitted dates conflict with other trip's dates", code='conflicitng_dates')
        return cd
                
        


class GroupJoinForm(forms.Form):
    group_key = forms.CharField(widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder':'Group Key here',
                                        'id':'Group_key'
                                    }),
                                max_length=10,
                                help_text='Enter Group Key to join'
                                ) 

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields='__all__'
        exclude=['owner', 'group', 'created_at']

class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photos
        fields = '__all__'
        exclude=['owner','group','event']

        widgets={
            'image':forms.ClearableFileInput(
                    attrs={
                        'class': 'form-control',
                        'type':'file',
                        'id':'formphoto',
                    }
            )}