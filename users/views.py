from urllib import request
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages

from .forms import UserLoginForm, UserRegistrationForm

# Create your views here.


def user_login(request):
    template_name = 'users/login.html'
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(request.POST)
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('store_main:index')
            print("User not authenticated")
    else:
        form = UserLoginForm()
    return render(request, template_name, { 'form': form })


def user_register(request):
    template_name = 'users/register.html'
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password1 = form.cleaned_data['password1']
            user = User.objects.create(email=email, first_name=first_name, last_name=last_name, password=password1)
            user.username = email
            user.save()

            login(request, user)
            return redirect('store_main:index')
        messages.error(request, "Unsuccessful registration. Please try again later.")
    else:
        # any other type of request
        form = UserRegistrationForm()
    return render(request, template_name, {'form': form})

def user_logout(request):
    if request.user:
        logout(request)
        return redirect('store_main:index')
