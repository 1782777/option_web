from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_view),
    path('json/', views.test),
]