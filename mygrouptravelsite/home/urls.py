from nturl2path import url2pathname
from django.urls import URLPattern, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomePage, name='home_page'),
    path('trips/', views.TripListView.as_view(), name='trip_list'),
    path('trips/my_trips/', views.UserTripListView.as_view(), name='user_trip_list'),
    path('trip_create/', views.TripCreateView.as_view(), name='trip_create'),
    path('trips/<int:pk>/', views.TripDetailView.as_view() , name='trip_detail'),
    path('trips/<int:pk>/update/', views.TripUpdateView.as_view(), name='trip_update'),
    path('trips/<int:pk>/delete/', views.TripDeleteView.as_view(), name='trip_delete'),
    path('trips/<int:pk>/members_list', views.TripMemberView.as_view(), name='trip_members'),
    path('trips/<int:pk>/event_create/', views.EventCreateView.as_view(), name='event_create'),
    path('trips/<int:pk>/event_list', views.EventListView.as_view(), name='event_list'),
    path('trips/<int:pk>/<int:pk_event>/', views.EventDetailView.as_view(), name='event_detail'),
    path('trips/<int:pk>/<int:pk_event>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('trips/<int:pk>/join/', views.TripJoin.as_view(), name='trip_join'),
    path('trips/<int:pk>/<int:pk_event>/vote/', views.Vote, name='vote'),
    path('trips/<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment_create_view'),
    path('trips/comment/<int:pk_comment>/like', views.AddLikeView.as_view(), name='comment_like'),
    path('trips/comment/<int:pk_comment>/unlike', views.DeleteLikeView.as_view(), name='comment_unlike'),
    path('trips/<int:pk>/upload_photo', views.PhotoView.as_view(), name='photo_upload'),
] 
