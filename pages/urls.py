from django.contrib import admin
from django.urls import path, include
from .views import HomeView, home_view

app_name = 'pages'

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view, name='home_view'),
]
