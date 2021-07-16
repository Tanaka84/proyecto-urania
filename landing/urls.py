from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('equipo', views.equipo, name="equipo"),
    path('herramientas', views.herramientas, name="herramientas")

]
