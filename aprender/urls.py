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
    path('folders/<int:id>', views.folder, name='folder'),
    path('<str:user>/sets', views.sets, name='sets'),
    path('sets/<int:id>', views.set, name='set'),
    path('sets/<int:id>/flashcards', views.flashcards, name='flashcards'),
    path('sets/<int:id>/learn', views.learn, name='learn'),
    path('sets/<int:id>/learn/restartLearnWay', views.restartLearnWay, name='restartLearnWay'),
    path('sets/<int:id>/learn/getWords', views.getWords, name='getwords'),
    path('sets/<int:id>/learn/check', views.check, name='check'),
    path('sets/<int:id>/test', views.test, name='test'),
    path('sets/<int:id>/nextWord', views.nextWord, name='nextWord'),
    path('sets/<int:id>/prevWord', views.prevWord, name='prevWord'),
    path('sets/<int:id>/currentWord', views.currentWord, name='currentWord'),
    path('<str:user>/fetchFoldersAjax', views.fetchFolders, name='fetchfolders'),
    path('<str:user>/fetchSetsAjax', views.fetchSets, name='fetchsets'),
    path('<str:user>', views.profile, name='profile'),
    path('<int:id>/createLearnPath', views.createLearnPath, name='createlearnpath'),
]
