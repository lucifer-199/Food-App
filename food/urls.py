from django.contrib import admin
from django.urls import path,include
from . import views
from food.views import *
from django.conf.urls import url

urlpatterns = [
    path('',views.home,name='home'),
    path('signup', views.handleSignup, name='handleSignup'),
    path('login', views.handleLogin, name='handleLogin'),
    path('logout', views.handleLogout, name='handleLogout'),
    url(r'^api/login/$',login.as_view(),name='login'),
    url(r'^api/register/$',RegisterUserView.as_view(),name='register new user'),
]