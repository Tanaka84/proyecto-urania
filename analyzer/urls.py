from django.urls import path

from . import views

urlpatterns = [
    path('twitter', views.twitter_fetch, name='twitter_fetch'),
    path('result', views.analyze, name = 'analyze' )
]
