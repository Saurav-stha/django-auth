from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllItems),
    path('add/', views.addItem),
    
    path('login', views.login),
    path('signup', views.signup),
    path('test_token', views.test_token),
    path('users', views.getAllUsers)
]
