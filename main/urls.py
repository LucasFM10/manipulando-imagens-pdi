# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('apply_negative', views.apply_negative, name='apply_negative'),
    path('apply_average', views.apply_average, name='apply_average'),
]
