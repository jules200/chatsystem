from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginview, name="login"),
    path('logout/', views.logoutview, name="logout"),    
    path('users', views.uuser, name="users"),
    path('delete/<user_id>', views.deleteuser, name="deleteuser"),
    path('editprofile', views.editprofile, name="editprofile"),
    path('new_account', views.new_account, name="new_account"),
]