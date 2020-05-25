from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_view),
    # path('json/', views.test),
    # path('save/', views.test_add_db),
    # path('load/', views.test_load_db),
    path('json/', views.get_ivmean),
    path('vol/', views.get_volume),
]
