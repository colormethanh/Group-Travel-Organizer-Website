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


class Group(models.Model):
    name = models.CharField(max_length=200, 
                            validators=[MinLengthValidator(3, "Group title must be longer than 3 characters")]
                            )
    
    key = models.CharField(max_length=10,
                            validators=[MinLengthValidator(3, "Group key must be longer than 3 characters")],
                            null=True
                            )
    description = models.TextField(max_length=200,
                            default="A cool group for a cool 'group' of people :)"
                            ) 
    # start_date = models.DateField(validators=[date_validator])
    # end_date = models.DateField(validators=[date_validator])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Going', related_name='members_going')

    def __str__(self):
        return self.name
    
    def ismember(self, user_id):
        member_lst = [member.id for member in self.members.all()]
        if user_id in member_lst:
            return True
        else:
            return False

    
class Event(models.Model):
    name = models.CharField(max_length=200, 
                            validators=[MinLengthValidator(3, "Event title must be longer than 3 characters")]
                            )
    description = models.TextField(max_length=200,
                            default='A cool event for a cool group of people :)'
                            )
    location= models.CharField(max_length=200, null=True)
    cost= models.DecimalField( max_digits=4 , decimal_places=2, default = 0)
    start_date = models.DateField(validators=[date_validator], null=True)
    end_date = models.DateField(validators=[date_validator], null=True)
    confirmed = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Voted', related_name='event_vote' )
    votes = models.IntegerField(default=0) 
    

    def __str__(self):
        return self.name
    
    def has_voted(self, user_id):
        voters_lst = [voter.id for voter in self.voters.all()]
        if user_id in voters_lst:
            return True
        else:
            return False


class Going(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '%s is a member of %s'%(self.user.username, self.group.name)

class Photos(models.Model):
    image = models.ImageField(upload_to='photos/')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_photos",null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_photos", null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'group_photo_{self.id}'


class Voted(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '%s voted on %s'%(self.user.username, self.event.name)


class Comment(models.Model):
    text = models.CharField(max_length=200,
                            validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
                            )
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Like', related_name='comment_liked')

    def __str__(self):
        return self.text

class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} likes {self.comment}"


