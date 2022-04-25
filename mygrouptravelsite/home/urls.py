from nturl2path import url2pathname
from django.urls import URLPattern, path
from . import views

name = 'home'

urlpatterns = [
    path('', views.HomePage, name='home_page' )
]