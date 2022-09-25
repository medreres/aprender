from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('createset', views.createset, name='createset'),
    path('createfolder', views.createfolder, name='createfolder'),
    path('<str:user>/folders', views.folders, name='folders'),
    path('<str:user>/folders/<int:id>', views.folder, name='folder'),
    path('<str:user>/sets', views.sets, name='sets'),
    path('<str:user>/sets/<int:id>', views.set, name='set'),
    path('<str:user>/fetchFoldersAjax', views.fetchFolders, name='fetchfolders'),
    path('<str:user>/fetchSetsAjax', views.fetchSets, name='fetchsets'),
    path('<str:user>', views.profile, name='profile')
]
