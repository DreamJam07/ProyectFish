from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
]

#Codigo que dectecta el mainpage