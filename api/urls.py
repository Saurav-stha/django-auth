from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllItems),
    path('add/', views.addItem)
]
