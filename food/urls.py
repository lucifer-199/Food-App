from django.contrib import admin
from django.urls import path,include
from . import views
from food.views import *
from django.conf.urls import url

urlpatterns = [
    path('',views.home,name='home'),
    path('signup', views.handleSignup, name='handleSignup'),
    path('login', HandleLoginView.as_view(), name='handleLogin'),
    path('logout', views.handleLogout, name='handleLogout'),
    path('token/verify/',TokenVerifyView.as_view(),name='token_verify'),
    path('results',DataView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
]