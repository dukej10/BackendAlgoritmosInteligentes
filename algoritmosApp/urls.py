#from django.conf.urls import urls
from django.urls import re_path as url
from algoritmosApp import views

urlpatterns = [
    url(r'^graph$', views.graphApi),
    url(r'^graph/([0-9]+)$', views.graphApi),
    url(r'^archivo$', views.simple_upload),
    url(r'^image$', views.img_upload),
    url(r'^imagexc$', views.img_ex),
    url(r'^randomgraph$', views.random_graph),
    url(r'^xml/([0-9]+)$', views.export_xml),
    url(r'^matriz/([0-9]+)$', views.export_matriz),
    url(r'^quey/([0-9]+)$', views.queyrannne),
    url(r'^cluster/([0-9]+)$', views.clustering),
    url(r'^puzzle-estrella$', views.algoritmo_estrella),
    url(r'^puzzle-anchura$', views.algoritmo_anchura),
    url(r'^puzzle-profundidad$', views.algoritmo_profundidad),
    url(r'^puzzle-primero$', views.algoritmo_primero),
]
