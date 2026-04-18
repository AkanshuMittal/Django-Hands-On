from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_weather, name='all_weather')
]