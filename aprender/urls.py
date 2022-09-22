from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginUser, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logoutUser, name='logout')
]
