from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import Trip, Event, Going, Comment
# Register your models here.

admin.site.register(Trip)
admin.site.register(Event)
admin.site.register(Going)
admin.site.register(Comment)