from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login),
    path('registrar', views.registrar),
    path('inicio', views.inicio),
    path('registro', views.registro),
    path('logout', views.logout),
    path('add', views.add),
]