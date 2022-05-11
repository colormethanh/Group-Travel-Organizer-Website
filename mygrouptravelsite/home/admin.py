from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import Group, Event, Going, Comment, Like, Photos
# Register your models here.

admin.site.register(Group)
admin.site.register(Event)
admin.site.register(Going)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Photos)