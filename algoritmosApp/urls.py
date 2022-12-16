#from django.conf.urls import urls
from django.urls import re_path as url
from algoritmosApp import views

urlpatterns = [
    url(r'^puzzle-estrella$', views.algoritmo_estrella),
    url(r'^puzzle-anchura$', views.algoritmo_anchura),
    url(r'^puzzle-profundidad$', views.algoritmo_profundidad),
    url(r'^puzzle-primero$', views.algoritmo_primero),
]
