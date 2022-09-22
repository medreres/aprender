from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from .models import User
from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import redirect
from django.contrib import messages #import messages

# Create your views here.


def index(request):
    # messages.success(request, "Success message")
    return render(request, 'aprender/index.html', {
        'LoginForm': LoginForm
    })


def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # check form for validity, else show error
        # TODO make alert if not valid
        if not form.is_valid():
            pass

        user = authenticate(
            request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            logUser(request, user)
        return HttpResponseRedirect(reverse('index'))

    # TODO process get request
    return render(request, 'aprender/login.html', {
        'LoginForm': LoginForm()
    })


def logoutUser(request):
    # log out and reverse back to main page
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        # TODO throw warning
        pass

        form = RegisterForm(request.POST)
        if not form.is_valid():
            # TODO throw an error
            pass

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
            # TODO handle error if user already exists
            pass

        logUser(request, user)
        # print(user)
        # redirect to main page
        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, 'aprender/register.html', {
            'RegisterForm': RegisterForm(),
            'LoginForm': LoginForm()
        })


def logUser(request,user):
    login(request, user)
    messages.success(request, f'You are now logged in as {user.username}')