from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#imports for authentication
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect

def home(request):
    return render(request, "index.html")

def login_view(request):
    """How we login to our app"""
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(f'/user/{u}')
                else:
                    print(f'{u} - account has been disabled')
                    return HttpResponseRedirect('/login')
            else:
                print('The username and/or password is incorrect')
                return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('/login')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', { 'form': form })
