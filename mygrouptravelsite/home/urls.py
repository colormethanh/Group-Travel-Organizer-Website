from nturl2path import url2pathname
from django.urls import URLPattern, path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomePage, name='home_page'),
    path('trips/', views.TripListView.as_view(), name='trip_list'),
    path('trips/my_trips/', views.UserTripListView.as_view(), name='user_trip_list'),
    path('trip_create/', views.TripCreateView.as_view(), name='trip_create'),
    path('trips/<int:pk>/', views.TripDetailView.as_view() , name='trip_detail'),
    path('trips/<int:pk>/update', views.TripUpdateView.as_view(), name='trip_update'),
    path('trips/<int:pk>/delete', views.TripDeleteView.as_view(), name='trip_delete'),
    path('trips/<int:pk>/event_create', views.EventCreateView.as_view(), name='event_create'),
    path('trips/<int:pk>/<int:pk_event>/update', views.EventUpdateView.as_view(), name='event_update'),
    path('trips/<int:pk>/join', views.TripJoin.as_view(), name='trip_join'),
]