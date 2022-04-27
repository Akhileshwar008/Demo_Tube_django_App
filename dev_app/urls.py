from django.urls import path
from . import views


urlpatterns = [
    # path('register/', views.register),
    path('home/', views.home),
    path('login/', views.login),
    path('login/loginsuccess/', views.loginsuccess),
    path('signup/', views.signup),
    path('signup/signupsuccess/', views.signupsuccess),
]


