from django.conf.urls.static import static
from django.urls import path

from app import views

urlpatterns = [
    path('signup/', views.SignUp, name='signup'),
    path('login/', views.Login, name='signup'),
    path('user/', views.UserDetails, name='User_Details'),
    path('post/',views.PostMethods.as_view(),name='Create_Tweet'),
    path('comment/',views.CommentMethods.as_view(),name='Create_Comment'),
    path('',views.UserFeed,name='UserFeed'),
]