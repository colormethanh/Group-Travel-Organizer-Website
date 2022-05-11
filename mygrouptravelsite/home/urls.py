from nturl2path import url2pathname
from django.urls import URLPattern, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomePage, name='home_page'),
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/my_groups/', views.UserGroupListView.as_view(), name='user_group_list'),
    path('group_create/', views.GroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/', views.GroupDetailView.as_view() , name='group_detail'),
    path('groups/<int:pk>/update/', views.GroupUpdateView.as_view(), name='group_update'),
    path('groups/<int:pk>/delete/', views.GroupDeleteView.as_view(), name='group_delete'),
    path('groups/<int:pk>/members_list', views.GroupMemberView.as_view(), name='group_members'),
    path('groups/<int:pk>/event_create/', views.EventCreateView.as_view(), name='event_create'),
    path('groups/<int:pk>/event_list', views.EventListView.as_view(), name='event_list'),
    path('groups/<int:pk>/<int:pk_event>/', views.EventDetailView.as_view(), name='event_detail'),
    path('groups/<int:pk>/<int:pk_event>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('groups/<int:pk>/join/', views.GroupJoin.as_view(), name='group_join'),
    path('groups/<int:pk>/<int:pk_event>/vote/', views.Vote, name='vote'),
    path('groups/<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment_create_view'),
    path('groups/comment/<int:pk_comment>/like', views.AddLikeView.as_view(), name='comment_like'),
    path('groups/comment/<int:pk_comment>/unlike', views.DeleteLikeView.as_view(), name='comment_unlike'),
    path('groups/<int:pk>/upload_photo', views.PhotoView.as_view(), name='photo_upload'),
] 
