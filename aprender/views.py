from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
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
        
        user = authenticate(request,username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
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
    return render(request, 'aprender/register.html', {
        'RegisterForm': RegisterForm()
    })