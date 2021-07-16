from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from urania import settings

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='signin'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
]
