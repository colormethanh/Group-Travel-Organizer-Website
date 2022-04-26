from nturl2path import url2pathname
from django.urls import URLPattern, path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomePage, name='home_page' ),
    path('trips/', views.TripListView.as_view(), name='trip_list' ),
    path('trip_create/', views.TripCreateView.as_view() , name='trip_create')
]