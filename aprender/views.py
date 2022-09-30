from ast import arg
from datetime import datetime
from doctest import debug_script
from operator import is_
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import LoginForm, RegisterForm, CreateSet, CreateFolder
from .models import Folder, User, Word, Set, LearnWay
from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import redirect
from django.contrib import messages  # import messages
from .helper import fetchSets, fetchFolders, createLearnPath, nextWord, currentWord, prevWord

# Create your views here.


def index(request):
    # messages.success(request, "Success message")
    return render(request, 'aprender/index.html', {
        'LoginForm': LoginForm,
        'CreateFolder': CreateFolder()
    })


def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # check form for validity, else show error
        if not form.is_valid():
            messages.error(request, "Error. Invalid form")

        user = authenticate(
            request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            logUser(request, user)
        else:
            messages.warning(
                request, "User with such password/username doesnt exist")
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'aprender/login.html', {
        'LoginForm': LoginForm()
    })


def logoutUser(request):
    # log out and reverse back to main page
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.user:
        messages.warning(request, 'You are already logged!')
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        # TODO throw warning
        pass

        form = RegisterForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Error. Invalid form")

        password = form.cleaned_data['password']
        password2 = form.cleaned_data['password2']
        if password != password2:
            # TODO throw an error
            # ? OR better to do it on frontend?
            pass

        # ? Check on front whether username is taken
        username = form.cleaned_data['username']

        # ? Check on front whether email is taken
        email = form.cleaned_data['email']

        # * register new user and sign in
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.warning(
                request, "User with such username already exists!")
            return HttpResponseRedirect(reverse('register'))

        logUser(request, user)
        # print(user)
        # redirect to main page
        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, 'aprender/register.html', {
            'RegisterForm': RegisterForm(),
            'LoginForm': LoginForm()
        })


def logUser(request, user):
    login(request, user)
    messages.success(request, f'You are now logged in as {user.username}')


def createset(request):
    if request.method == 'POST':
        form = CreateSet(request.POST)
        

        if not form.is_valid():
            messages.error(request, 'Form is not valid')
            return HttpResponseRedirect(reverse('createset'))

        # ! CRUTCHES
        formFields = request.POST
        # didn't manage to implement correctly, so all terms and their definitions
        # will be fetched via request.POST than it would be better to do via django form

        # iterate through all terms and create corresponding object Word
        wordsObjectList = []
        for (word, definition) in zip(formFields.getlist('words'), formFields.getlist('definitions')):
            # create Word model for every word-definition
            wordModel = Word.objects.create(term=word, definition=definition)
            wordsObjectList.append(wordModel)

        studySet = Set.objects.create(
            label=form.cleaned_data['label'],
            date=datetime.now(),
            author=request.user,
            description=form.cleaned_data['description']
        )
        studySet.words.add(*[w.id for w in wordsObjectList])

        return HttpResponseRedirect(reverse('createset'))

    return render(request, 'aprender/createset.html', {
        'CreateSet': CreateSet(),
    })


def sets(request, user):
    return render(request, 'aprender/sets.html',
                  {
                      'CreateFolder': CreateFolder()
                  })


def set(request, id):
    # find out if user has already started learning way
    return render(request, 'aprender/set.html', {
        'set': Set.objects.get(pk=id).serialize(),
        'learnStarted': LearnWay.objects.filter(author=request.user).filter(set__pk=id).count() > 0,
        'id': id
    })


def createfolder(request):
    if request.method != "POST":
        messages.error(request, 'Error. Wrong request method')
        return HttpResponseRedirect(reverse('index'))

    form = CreateFolder(request.POST)
    if not form.is_valid():
        messages.error(request, 'Error. Form is not valid')

    folder = Folder.objects.create(
        label=form.cleaned_data['label'],
        description=form.cleaned_data['description'],
        author=request.user,
        date=datetime.now()
    )

    return HttpResponseRedirect(reverse('folders', args=(request.user,)))


def folders(request, user):
    return render(request, 'aprender/folders.html', {
        'username': user,
    })


def folder(request, id):
    return HttpResponse("TODO")


def profile(request, user):
    return render(request, 'aprender/profile.html')


def flashcards(request,id):
    return render(request, 'aprender/flashcards.html')