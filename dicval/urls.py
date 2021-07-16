from django.urls import path

from . import views

urlpatterns = [
    path('', views.entrada, name='entrada'),
    path('pres', views.presentacion, name='presentacion'),
    path('votos', views.pagina_de_votos, name='voto'),
    path('despedida', views.cierre, name='cierre')
]
