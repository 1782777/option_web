from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_view),
    path('fuwu/', views.test_view),
]