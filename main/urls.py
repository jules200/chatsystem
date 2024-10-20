from turtle import home
from django.urls import path
from .import views
from .views import FeedListCreateView, FeedDetailView

urlpatterns = [
    path('', views.main, name="main"),
    path('messages', views.messages, name="messages"),
    path('friends', views.friends, name="friends"),
    path('new_friends', views.new_friends, name="new_friends"),
    path('followers', views.followers, name="followers"),
    path('new_post', views.newpost, name="new_post"),
    path('delete_post/<int:post_id>', views.deletepost, name="delete_post"),
    path('insert_comment', views.insert_comment, name="insert_comment"),
    path('feedlikes/<int:feed_id>', views.feedlikes, name="feedlikes"),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('feeds/', FeedListCreateView.as_view(), name='feed-list-create'),
    path('feeds/<int:pk>/', FeedDetailView.as_view(), name='feed-detail'),
]